from datetime import datetime

from src.dao.twitter_dao import UserTable, UserDetailsTable, FollowerDetailsTable, TweetDetailsTable
from src.lib.password_helpers import encrypt_password, decrypt_password
from src.model.twitter import User, UserDetails, FollowerDetails, TweetDetails

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def user_object_maker(user_name, password):
    user_object = User()
    user_object.user_name = user_name
    user_object.password = password
    return user_object


def user_details_object_maker(user_name, user_id):
    user_details_object = UserDetails()
    user_details_object.user_name = user_name
    user_details_object.user_id = user_id
    user_details_object.created_at = datetime.now().strftime(DATE_FORMAT)
    return user_details_object


def follower_details_object_maker(user_name, following_name):
    follower_details_object = FollowerDetails()
    follower_details_object.user_name = user_name
    follower_details_object.following_name = following_name
    follower_details_object.followed_at = datetime.now().strftime(DATE_FORMAT)
    return follower_details_object


def tweet_details_object_maker(user_name, tweet_msg):
    tweet_details_object = TweetDetails()
    tweet_details_object.user_name = user_name
    tweet_details_object.tweet_msg = tweet_msg
    tweet_details_object.twitted_at = datetime.now().strftime(DATE_FORMAT)
    return tweet_details_object


def validate_login_user(user_name, password):
    u_obj = UserTable()
    user = u_obj.get_user_details(user_name)
    if user:
        passwd = decrypt_password(user.password)
        if passwd == password:
            return True, 'Welcome {}!'.format(user_name)
        else:
            return False, 'Invalid password or user name'
    else:
        return 'User {} not found'.format(user_name)


def add_new_user(user_name, password):
    u_obj = UserTable()
    ud_obj = UserDetailsTable()
    user = user_object_maker(user_name, encrypt_password(password))
    user_resp = u_obj.create_new_user(user)
    user = u_obj.get_user_details(user_name)
    user_details = user_details_object_maker(user_name, user.user_id)
    user_details_resp = ud_obj.create_new_user(user_details)
    if user_resp and user_details_resp:
        return True
    return False


def get_all_tweets(session):
    fd_obj = FollowerDetailsTable()
    td_obj = TweetDetailsTable()
    followers = fd_obj.get_followers_details(session.get('username'))
    followers = [follower.following_name for follower in followers]
    tweets = td_obj.get_tweets(followers)
    tweets_final = []
    if tweets:
        for tweet in tweets:
            t = {}
            t['tweet_msg'] = tweet.tweet_msg
            t['twitted_at'] = tweet.twitted_at
            t['user_name'] = tweet.user_name
            tweets_final.append(t)
    return tweets_final


def post_user_tweet(session, tweet_msg):
    if not tweet_msg or len(tweet_msg) > 140:
        return 'Empty tweet or length of tweet exceeds 140', 403
    td_obj = TweetDetailsTable()
    ud_obj = UserDetailsTable()
    tweet = tweet_details_object_maker(session.get('username'), tweet_msg)
    tweet_resp = td_obj.set_tweet(tweet)
    tweet_count_resp = ud_obj.update_tweet_count(session.get('username'))
    if tweet_resp and tweet_count_resp:
        return 'Twitted Successfully!', 200
    return 'Failed saving the tweet', 500


def add_follower(session, follower_name):
    ud_obj = UserDetailsTable()
    if ud_obj.get_user_details(follower_name):
        fd_obj = FollowerDetailsTable()
        follower = follower_details_object_maker(session.get('username'), follower_name)
        follower_resp = fd_obj.set_follower_details(follower)
        following_count_resp = ud_obj.update_following_count(session.get('username'))
        follower_count_resp = ud_obj.update_followers_count(follower_name)
        if follower_resp and following_count_resp and follower_count_resp:
            return 'You started following {}'.format(follower_name), 200
        return 'Request to follow {} failed'.format(follower_name), 500
    return '{} user name not found'.format(follower_name), 403
