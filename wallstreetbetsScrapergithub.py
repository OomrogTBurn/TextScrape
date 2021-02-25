import pandas as pd
import praw
import os

os.chdir("C:/Users/jfalk/Documents")

# create a reddit connection
reddit = praw.Reddit(
    client_id='', 
    client_secret='', 
    user_agent=''
)


# =============================================================================
# Host of basic commands. Keeping here to keep track of
# =============================================================================

#create instance pointing at a specified subreddit
subreddit = reddit.subreddit("wallstreetbets")

#print(subreddit.display_name)  
#print(subreddit.title)         
#print(subreddit.description)   



# =============================================================================
# Quick pulling top 100 hot posts and throwing them into a dataframe
# =============================================================================
'''
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
    '''
'''
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
# posts.to_csv("testposts.csv")
'''

# =============================================================================
# Scraping comments from post
# =============================================================================

submission = reddit.submission(id="lra5cg")


submission.comments.replace_more(limit=3)
for comment in submission.comments.list():
    print(comment.body)
