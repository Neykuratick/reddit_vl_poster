import requests

from enum import Enum
from typing import Optional

from pydantic.class_validators import List
from pydantic.class_validators import validator
from pydantic.main import BaseModel


class PostHints(str, Enum):
    IMAGE = 'image'
    GIF = 'gif'
    UNKNOWN = 'unknown'


class RedditPost(BaseModel):
    title: str
    link_flair_text: Optional[str] = None
    url_overridden_by_dest: str  # media url
    post_hint: str
    media_bytes: Optional[bytes] = None

    @validator('title')
    def validate_title(cls, v):
        """ Убирает точку с конца предложения """

        last_char = v[-1]
        if last_char == '.':
            return v[:-1]

        return v

    @validator('post_hint')
    def validate_post_hint(cls, v, values):
        url = values.get('url_overridden_by_dest')
        extension = url.split('.')[-1]

        if extension in ('jpg', 'jpeg', 'png'):
            return PostHints.IMAGE
        elif extension == 'gif':
            return PostHints.GIF
        else:
            return PostHints.UNKNOWN

    @validator('media_bytes', always=True, pre=True)
    def validate_media_bytes(cls, v, values):
        url = values.get('url_overridden_by_dest')
        print(f'RedditPost validator: downloading {url=}')

        result = requests.get(url, stream=True)
        if isinstance(result.content, bytes):
            return result.content

        raise ValueError(f'Media bytes are empty. {result.text=} {result.content=}')


def get_posts(subreddit) -> List[RedditPost]:
    url = f"https://www.reddit.com/r/{subreddit}/.json"
    response = requests.get(url, headers={'User-Agent': 'MyRedditScraper'}).json()

    posts_raw = response.get('data').get('children')
    result = []
    hint_whitelist = [PostHints.IMAGE, PostHints.UNKNOWN]

    for post in posts_raw[1:]:
        post_model = RedditPost(**post.get('data'))
        if post_model.post_hint in hint_whitelist:
            result.append(post_model)
            
            if post_model.post_hint == PostHints.UNKNOWN:
                print(f"\n\n{post_model.post_hint=}\n\n")
    
    return result

