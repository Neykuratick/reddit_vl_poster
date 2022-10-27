import requests

from app.reddit import RedditPost
from app.utils import get_timestamp
from config import settings


def get_upload_link() -> str:
    data = {
        "group_id": settings.COMMUNITY_ID,
        "access_token": settings.VK_TOKEN,
        "v": "5.131",
    }

    response = requests.post(
        "https://api.vk.com/method/photos.getWallUploadServer", data=data
    )
    json = response.json()
    return json.get("response").get("upload_url")


def upload_photo(photo: bytes):
    url = get_upload_link()
    data = {"photo": ("test.png", photo)}
    data = requests.post(url, files=data).json()
    payload = {
        "access_token": settings.VK_TOKEN,
        "group_id": settings.COMMUNITY_ID,
        "photo": data.get("photo").replace("\\", ""),
        "server": data.get("server"),
        "hash": data.get("hash"),
        "v": 5.131,
    }

    # загрузили фото на сервер
    response = requests.post(
        "https://api.vk.com/method/photos.saveWallPhoto", data=payload
    )
    return response.json()


def post_meme(post: RedditPost, hours_delta: int) -> dict:
    response = upload_photo(post.media_bytes)
    data = response.get("response")[0]
    owner_id = data.get("owner_id")
    photo_id = data.get("id")

    payload = {
        "access_token": settings.VK_TOKEN,
        "message": post.title,
        "attachments": f"photo{owner_id}_{photo_id}",
        "owner_id": f"-{settings.COMMUNITY_ID}",
        "from_group": 1,
        "publish_date": get_timestamp(hours_delta=hours_delta),
        "v": 5.131,
    }

    response = requests.post("https://api.vk.com/method/wall.post", data=payload)
    return response.json()
