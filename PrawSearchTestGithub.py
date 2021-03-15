import pandas as pd
import praw
import os
from re import search

os.chdir("")

# create a reddit connection
reddit = praw.Reddit(
    client_id='', 
    client_secret='', 
    user_agent=''
)


Checkthread = 'Daily'

#create instance pointing at a specified subreddit
subreddit = reddit.subreddit("wallstreetbets")

submissionlist = []

for submission in reddit.subreddit("wallstreetbets").search("flair:Daily Discussion", limit=None):
    submissionlist.append(
            [
                submission.id,
                submission.title,
                submission.created_utc
            ]
        )

    #Dataframe for exporting
    submissiondf = pd.DataFrame(
        submissionlist,
        columns=[
            "id",
            "Title",
            "posttime"
        ],
    )

    submissiondf['realdatetime'] = pd.to_datetime(submissiondf['posttime'], unit='s')

submissiondf.to_csv('wallstreetbetssubids.csv', index=False)
