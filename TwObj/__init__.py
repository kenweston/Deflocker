from threading import Timer
from rauth import OAuth1Service as oauth

# Robert Kenneth Weston
# Twitter Object declarations

""" Object Declarations """

class User:
    def __init__(self, user_id):
        # available values from REST API
        self.name = None
        self.profile_image_url = None
        self.follow_request_sent = None
        self.user_id = user_id
        self.favourites_count = None
        self.profile_image_url = None
        self.lang = None
        self.followers_count = None
        self.protected = None
        self.notifications = None
        self.verified = None
        self.geo_enabled = None
        self.time_zone = None
        self.description = None
        self.default_profile_image = None
        self.statuses_count = None
        self.friends_count = None
        self.following = None
        self.screen_name = None
        self.status = None
        
        # generated values
        self.followers = None
        self.friends = None
        self.latest_tweet = None
        self.tweets = None
        self.favourites = None
    
class AuthenticatingUser(User):
    def __init__(self, user_id):
        self.pending_friendships = None
        User.__init__(self, user_id)
    
class Tweet:
    def __init__(self, tweet_id):
        self.tweet_id = tweet_id
        self.created_at = None
        self.in_reply_to_user_id = None
        self.text = None
        self.in_reply_to_status_id = None
        self.retweet_count = None
        self.retweeted = None
        self.in_reply_to_screen_name = None