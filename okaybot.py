import config
import json
import praw
from praw.models import MoreComments
from os.path import dirname, abspath

userAgent = 'Look at popular comments that may get deleted'
clientID = config.client_id
clientSecret = config.client_secret
userName = config.username
userPassword = config.password

d = dirname(abspath(__file__))
print(d)

# takes comment and counts total number of silver, gold, plat awards
def count_awards(comm):
    return sum(comm.gildings.values())

r = praw.Reddit(user_agent = userAgent, client_id = clientID, client_secret = clientSecret, username = userName, password = userPassword)

sub = r.subreddit('askreddit')
c_dict = {}

# parent id, awards, points, body, deleted
#class my_comment():
    # parent_id = ''
    # awards = 0
    # points = 0
    # body = ''
    # deleted = False
    # def __init__(self, parent_id, awards, points, body):
    #     self.parent_id = parent_id
    #     self.awards = awards
    #     self.points = points
    #     self.body = body
    
    # def set_awards(self, awards):
    #     self.awards = awards
    # def set_points(self, points):
    #     self.points = points
    # def set_del():
    #     self.deleted = True

def my_comment(p_id, awa, points, body, deleted):
    return {
        "parent_id": p_id,
        "awards": awa,
        "points": points,
        "body": body,
        "deleted": deleted
    }

def read():
    with open(d + '/dict.json', 'r+') as f:
        c_dict = json.load(f)

def start():
    for submission in sub.hot(limit=20):
        p_id = submission.id
        for comments in submission.comments:
            if isinstance(comments, MoreComments):
                continue
            if (comments.score > 3000) or (count_awards(comments) > 3):
                c_dict.update({comments.id : my_comment(p_id, count_awards(comments), comments.score, comments.body, False)})

def write():
    with open(d + '/dict.json', 'w') as f:
        json.dump(c_dict, f)

def check_del(id):
    return r.comment(id).body == "[deleted]"

# read()
# #start()
# write()


# comments by id
# comment = r.comment('h9my5ub')
# print(comment.score)

# for c in r.redditor("reddit").comments.new(limit=3):
#     print(c.id, " : ", c.body)

# dictionary with
# key: comment id
# value: my_comment