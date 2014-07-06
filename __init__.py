import json
import datetime as dt
import urllib.request
import urllib.parse

from threading import Timer
from rauth import OAuth1Service as oauth

from Deflocker.TwObj import User
from Deflocker.TwObj import AuthenticatingUser
from Deflocker.TwObj import Tweet

""" Constant Declarations """
MAX_ID_LIST_COUNT = 5000
MAX_DETAILED_LIST_COUNT = 200
MAX_IDS_PER_REQUEST = 100

""" API Constant Declarations """
URL = "https://userstream.twitter.com/1.1/"
FRIENDS_IDS = "friends/ids.json"
FOLLOWERS_IDS = "followers/ids.json"
FRIENDSHIPS_OUTGOING = "friendships/outgoing.json"
STATUSES_USER_TIMELINE = "statuses/user_timeline.json"
USERS_LOOKUP = "users/lookup.json"
        
def download_followers(user):
    user.followers = _get_id_list_helper(self, FOLLOWERS_IDS, user_id = user.user_id, count = MAX_ID_LIST_COUNT, stringify_ids = True)
    user.followers_count = len(self.followers)
        
def download_friends(user):
    user.friends = _get_id_list_helper(self, FOLLOWERS_IDS, user_id = user.user_id, count = MAX_ID_LIST_COUNT, stringify_ids = True)
    user.friends_count = len(self.friends)
    
def download_timeline(user, n_tweets = 200):
    if n_tweets > MAX_DETAILED_LIST_COUNT:
        # throw an exception or a warning
        n_tweets = 200
    options = {user_id : user.user_id,
               count : n_this_request,
               trim_user : True,
               include_rts : True,
               next_cursor : next_cursor}
        
    info = __send_get_request__(URL, STATUSES_USER_TIMELINE, options)
        
    # extract tweets from information
    
def download_favourite_tweets(user):
    pass

def login(username, password):
    return AuthenticatingUser(username, password)

def download_pending_friendships(authenticating_user):
    if type(authenticating_user) is not Deflocker.TwObj.AuthenticatingUser:
        return None
    else:
        authenticating_user.pending_friendships = _get_id_list_helper(self, FRIENDSHIPS_OUTGOING, stringify_ids = True)

def download_bulk_user_info(dict_of_users):
    list_of_ids = _list_of_keys(dict_of_users)
    proper_length_lists = _seperate_lists(list_of_ids, MAX_IDS_PER_REQUEST)
    
    for l in proper_length_lists:
        request_string = ""
        for u in l:
            request_string += u + ","
        # remove the last comma
        request_string = request_string[:len(request_string)-1]
        
        # send post request
        doc = _send_post_request(None)
        
        for entry in doc:
            user = dict_of_users[entry["id_str"]]
            # extract relevant information
            user.name = entry["name"]
            user.profile_image_url = entry["profile_image_url"]
            user.follow_request_sent = entry["follow_request_sent"]
            user.favourites_count = entry["favourites_count"]
            user.profile_image_url = entry["profile_image_url"]
            user.lang = entry["lang"]
            user.followers_count = entry["followers_count"]
            user.protected = entry["protected"]
            user.notifications = entry["notifications"]
            user.verified = entry["verified"]
            user.geo_enabled = entry["geo_enabled"]
            user.time_zone = entry["time_zone"]
            user.description = entry["description"]
            user.default_profile_image = entry["default_profile_image"]
            user.statuses_count = entry["statuses_count"]
            user.friends_count = entry["friends_count"]
            user.following = entry["following"]
            user.screen_name = entry["screen_name"]
            
            # construct user's last tweet
            status = Tweet(entry["status"]["id_str"])
            status.created_at = None
            status.in_reply_to_user_id = entry["status"]["in_reply_to_user_id_str"]
            status.text = entry["status"]["text"]
            status.in_reply_to_status_id = entry["status"]["in_reply_to_status_id_str"]
            status.retweet_count = entry["status"]["retweet_count"]
            status.retweeted = entry["status"]["retweeted"]
            status.in_reply_to_screen_name = entry["status"]["in_reply_to_screen_name"]
            
            user.status = status
            
""" Helper Function Declarations """   

# send GET request
# input: the api url, the api command file, a dictionary mapping the options
# returns JSON doc
def __send_get_request__(url, command, options):
    options_str = urllib.parse.urlencode(options)
    # alter boolean values to accomodate Twitter API
    options_str.replace('True', 'true').replace('False','false')
    request = url + command + "?" + urllib.parse.urlencode(options)
    
    result = urllib.request.urlopen(url)
    return result

def _send_post_request(url, command, data):
    data_str = urllib.parse(urlencode(options))
    data_str.replace('True', 'true').replace('False','false')   
    
    result = urllib.request.urlopen(url + command, data = data_str)
    return result

def _create_dict( **args ):
    empty_vals = []
    for key in args:
        if args[key] is None:
            empty_vals.append(key)
    for arg in empty_vals:
        del args[key]
    del empty_vals
    return args

def _list_of_keys(dictionary):
    l = []
    for key in dictionary:
        l.append(key)
    return l

# helper function to collect all possible information and exhaust the cursors
# returns a list
def _get_all_information(url, function, options, info_location):
    info = []
    next_cursor = -1
    
    while next_cursor:
        doc = json.load(__send_get_request__(URL, function, options))
        for item in doc[info_location]:
            info.append(item)
            
        next_cursor = doc["next_cursor"]
        options["cursor"] = doc["next_cursor_str"]
            
    return info

def _get_id_list_helper(function, user_id = None, screen_name = None, cursor = None, stringify_ids = None, count = None):
    # compile list of options supplied to function
    options = _create_dict(user_id = user_id, 
                           screen_name = screen_name,
                           cursor = cursor,
                           stringify_ids = stringify_ids,
                           count = count)
    
    # if stringify_ids is True, then extract information from ids_str
    location = None
    if stringify_ids:
        location = "ids_str"
    else:
        location = "ids"
        
    return _get_all_information(URL, function, options, location)

def _seperate_lists(list_of_info, max_list_size):
    collection_of_lists = []
    
    current_list = []
    for item in list_of_info:
        # add item to the current list
        current_list.append(item)
        # if the current list has reached max size, then store it and start a new list
        if len(current_list) == max_list_size:
            collection_of_lists.append(current_list)
            current_list = []
            print("next list")
            
            
    return collection_of_lists




""" Main Program 

# login user
my_user = User("id here")

# download friends and followers
my_user.download_friends()
my_user.download_followers()

friends = user.get_friends()
followers = user.get_followers()

non_mutual = []

for user_id in friends:
    if user_id not in followers:
        non_mutual.append(user_id)

possible_deletions = {}
for user_id in non_mutual:
    possible_deletions[user_id] = User(user_id) """
    
