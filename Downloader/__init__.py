from rauth import OAuth1Service as oauth
import urllib.request
import urllib.parse

from threading import Timer

""" Constant Declaration """
RATE_LIMIT_WINDOW = 15.0 * 60.0 # 15 minutes

URL = "https://userstream.twitter.com/1.1/"
FRIENDS_IDS = "friends/ids.json"
FOLLOWERS_IDS = "followers/ids.json"
FRIENDSHIPS_OUTGOING = "friendships/outgoing.json"
STATUSES_USER_TIMELINE = "statuses/user_timeline.json"
USERS_LOOKUP = "users/lookup.json"

def start_oauth_service():
    consumer_key = input()
    consumer_secret = input()
    
    service = oauth(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  name='twitter',
                  access_token_url='https://api.twitter.com/oauth/access_token',
                  request_token_url='https://api.twitter.com/oauth/request_token',
                  base_url='https://api.twitter.com/1/')
    
    return service


def send_oauth_verifier(service):
    request_token, request_token_secret = service.get_request_token()
    # print url
    print("https://api.twitter.com/oauth/authorize?oauth_token=" + request_token)
    pin=input()
    request_token, request_token_secret = service.get_request_token()
    data={'oauth_verifier':pin, 'oauth_token':request_token}
    data = bytes(urllib.parse.urlencode(data), 'ascii')
    return urllib.request.urlopen('https://api.twitter.com/oauth/access_token',data=data)
'''
class DownloadRequest:
    def __init__(self, requesting_object, requesting_function, url, command, options = None, data = None):
        # construct Request
        request_str = url + command
        
        if options is not None:
            options_str = urllib.parse.urlencode(options)
            options_str.replace('True', 'true').replace('False','false')
            request_str += "?" + options_str
            
        if data is not None:
            data_str = urllib.parse((urlencode(data))
            data_str.replace('True', 'true').replace('False','false')   
            result = urllib.request.urlopen(url, data = data_str)
        else:
            data_str = None
        
        request = urllib.request.Request(request_str, data_str, headers= {})
        
        # schedule request
        t = Timer(1.0, execute_search, [requesting_object, requesting_function, request])
        t.start()
        
    def execute_search(self, requesting_object, requesting_function, request):
        result = urllib.request.urlopen(request)
        requesting_function(requesting_object, result)'''