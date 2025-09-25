import praw
import os
from typing import List


def authenticate_reddit():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT', 'sentiment_map by /u/yourusername')
    )
    return reddit


def fetch_posts_from_subreddit(reddit, subreddit: str, limit: int = 100) -> List[dict]:
    posts = []
    for submission in reddit.subreddit(subreddit).new(limit=limit):
        posts.append({
            'id': submission.id,
            'title': submission.title,
            'url': submission.url,
            'content': submission.selftext or submission.title,
            'created_utc': submission.created_utc,
            'score': submission.score,
            'subreddit': subreddit
        })
    return posts


def collect_reddit_data(provinces_config: List[dict], limit: int = 100) -> List[dict]:
    """Collect posts for each province's subreddit.

    provinces_config: list of {'name': <province>, 'subreddit': <subreddit>}
    returns: list of posts with added 'province' field
    """
    reddit = authenticate_reddit()
    all_posts = []
    for p in provinces_config:
        name = p.get('name')
        subreddit = p.get('subreddit')
        try:
            posts = fetch_posts_from_subreddit(reddit, subreddit, limit=limit)
            for post in posts:
                post['province'] = name
            all_posts.extend(posts)
        except Exception:
            # If subreddit fails, continue with others
            continue
    return all_posts