import pandas as pd
import praw
import os

os.chdir("")

# create a reddit connection
reddit = praw.Reddit(
    client_id='', 
    client_secret='', 
    user_agent=''
)

#create instance pointing at a specified subreddit
subreddit = reddit.subreddit("wallstreetbets") 


# =============================================================================
# Scraping comments from post
# =============================================================================

#Empty list to hold comment and ID
commentlist = []

subIds = ['lwr7oo', 'lvzh9h']

for subID in subIds:


    #Daily post thread 2/25/2021
    submission = reddit.submission(id=subID)

    #Sorting newest comments to the top
    submission.comment_sort = 'new'

    #Creating comments list object
    submission.comments.replace_more(limit=None)
    comments = submission.comments.list()

    

    for comment in comments:
        commentlist.append(
            [
                comment.id,
                comment.body,
                comment.created_utc
            ]
        )

#Dataframe for exporting
commentdf = pd.DataFrame(
    commentlist,
    columns=[
        "id",
        "text",
        "posttime"
    ],
)

commentdf['realdatetime'] = pd.to_datetime(commentdf['posttime'], unit='s')
#Extracting hour and day from dateimt
commentdf['posthour'] = commentdf['realdatetime'].dt.hour
commentdf['postday'] = commentdf['realdatetime'].dt.day

commentdf = commentdf.drop(columns={'posttime'})

#append commentdf to a big dataframe outside the loop



commentdf.to_csv('wsb2posts2021.csv', index=False)

