from app.reddit import get_posts
from app.vk import post_meme


def drive():
    posts = get_posts("dankmemes")
    posts_count = len(posts)
    fail = ""

    for index, post in enumerate(posts):
        result = post_meme(post=post, hours_delta=index)
        if "post_id" in result.get("response"):
            print(
                f"{post.title, post.url_overridden_by_dest} - SUCCESS ({index}/{posts_count})"
            )
        else:
            fail += f"{post.title, post.url_overridden_by_dest} - FAILED ({index}/{posts_count})\n"

    if fail:
        print(f"FAILS:\n{fail}")
