# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 19:51:56 2021

@author: jfalk

Attempting some Reddit scraping and basic text analysis
"""

import praw
import pandas as pd
import spacy

# create a reddit connection
reddit = praw.Reddit(
    client_id='W_UUi-3Ujow1NA', 
    client_secret='Q6ElYPJUnzWGpK1zV2Eis5ytjBm87g', 
    user_agent='StonkScrape'
)

# list for df conversion
posts = []
# return 100 new posts from wallstreetbets
new_bets = reddit.subreddit("wallstreetbets").new(limit=100)
# return the important attributes
for post in new_bets:
    posts.append(
        [
            post.id,
            post.author,
            post.title,
            post.score,
            post.num_comments,
            post.selftext,
            post.created,
            post.pinned,
            post.total_awards_received,
        ]
    )

# create a dataframe
posts = pd.DataFrame(
    posts,
    columns=[
        "id",
        "author",
        "title",
        "score",
        "comments",
        "post",
        "created",
        "pinned",
        "total awards",
    ],
)

posts["created"] = pd.to_datetime(posts["created"], unit="s")
posts["created date"] = pd.to_datetime(posts["created"], unit="s").dt.date
posts["created time"] = pd.to_datetime(posts["created"], unit="s").dt.time
posts = posts.loc[posts['post'] !='']
