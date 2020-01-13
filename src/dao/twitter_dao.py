from sqlalchemy import desc

from src.constants.database_constants import USER_TABLE_NAME, USER_DETAILS_TABLE_NAME, TWEET_DETAILS_TABLE_NAME, \
    FOLLOWER_DETAILS_TABLE_NAME
from src.lib.pg_connection import connect_pg, session_maker
from src.lib.log_conf import log
from src.model.twitter import User, UserDetails, FollowerDetails, TweetDetails


class UserTable():

    def __init__(self):
        pg_connection = connect_pg()
        if not pg_connection.dialect.has_table(pg_connection, USER_TABLE_NAME):
            User.__table__.create(pg_connection)
            log.info("User Table Created")

    def get_user_details(self, user_name):
        session = session_maker()
        try:
            user = session.query(User).filter(User.user_name == user_name)
            return user.first()
        except Exception as e:
            log.info("User {} not found".format(user_name))
            log.exception("Exception while getting user {} message {}".format(user_name, e.message))
        finally:
            session.close()

    def create_new_user(self, user):
        session = session_maker()
        try:
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            log.exception("Exception while creating new user {} message {}".format(user.user_name, e.message))
            print user.password
        finally:
            session.close()


class UserDetailsTable():

    def __init__(self):
        pg_connection = connect_pg()
        if not pg_connection.dialect.has_table(pg_connection, USER_DETAILS_TABLE_NAME):
            UserDetails.__table__.create(pg_connection)
            log.info("User Details Table Created")

    def get_user_details(self, user_name):
        session = session_maker()
        try:
            user_datails = session.query(UserDetails).filter(UserDetails.user_name == user_name)
            return user_datails.first()
        except Exception as e:
            log.info("User {} not found".format(user_name))
            log.exception("Exception while getting user {} message {}".format(user_name, e.message))
        finally:
            session.close()

    def create_new_user(self, user):
        session = session_maker()
        try:
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            log.exception("Exception while creating new user {} message {}".format(user.user_name, e.message))
        finally:
            session.close()

    def update_followers_count(self, user_name):
        session = session_maker()
        try:
            row = session.query(UserDetails).filter(UserDetails.user_name == user_name).first()
            row.followers += 1
            session.commit()
            return True
        except Exception as e:
            log.exception("Exception while updating follower data for user {} message {}".format(user_name, e.message))
        finally:
            session.close()

    def update_following_count(self, user_name):
        session = session_maker()
        try:
            row = session.query(UserDetails).filter(UserDetails.user_name == user_name).first()
            row.following += 1
            session.commit()
            return True
        except Exception as e:
            log.exception("Exception while updating following data for user {} message {}".format(user_name, e.message))
        finally:
            session.close()

    def update_tweet_count(self, user_name):
        session = session_maker()
        try:
            row = session.query(UserDetails).filter(UserDetails.user_name == user_name).first()
            row.tweets += 1
            session.commit()
            return True
        except Exception as e:
            log.exception("Exception while updating tweet data for user {} message {}".format(user_name, e.message))
        finally:
            session.close()


class FollowerDetailsTable():

    def __init__(self):
        pg_connection = connect_pg()
        if not pg_connection.dialect.has_table(pg_connection, FOLLOWER_DETAILS_TABLE_NAME):
            FollowerDetails.__table__.create(pg_connection)
            log.info("Follower Details Table Created")

    def get_followers_details(self, user_name):
        session = session_maker()
        try:
            query = session.query(FollowerDetails).filter(FollowerDetails.user_name == user_name)
            return query.all()
        except Exception as e:
            log.exception("Exception while getting followers details for {} message {}".format(user_name, e.message))
        finally:
            session.close()

    def set_follower_details(self, follower):
        session = session_maker()
        try:
            session.add(follower)
            session.commit()
            return True
        except Exception as e:
            log.exception("Exception while adding new follower {} for user {} message {}"
                          .format(follower.following_name, follower.user_name, e.message))
        finally:
            session.close()


class TweetDetailsTable():

    def __init__(self):
        pg_connection = connect_pg()
        if not pg_connection.dialect.has_table(pg_connection, TWEET_DETAILS_TABLE_NAME):
            TweetDetails.__table__.create(pg_connection)
            log.info("Tweet Details Table Created")

    def get_tweets(self, user_names):
        session = session_maker()
        try:
            query = session.query(TweetDetails).filter(TweetDetails.user_name.in_(user_names))\
                .order_by(desc(TweetDetails.twitted_at))
            return query.all()
        except Exception as e:
            log.exception("Exception while getting tweets message {}".format(e.message))
        finally:
            session.close()

    def set_tweet(self, tweet):
        session = session_maker()
        try:
            session.add(tweet)
            session.commit()
            return True
        except Exception as e:
            log.exception("Exception while adding new tweet {} for user {} message {}"
                          .format(tweet.tweet_msg, tweet.user_name, e.message))
        finally:
            session.close()
