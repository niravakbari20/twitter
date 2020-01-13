from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKeyConstraint, BigInteger, PrimaryKeyConstraint

from src.constants.database_constants import USER_TABLE_NAME, USER_DETAILS_TABLE_NAME, TWEET_DETAILS_TABLE_NAME, \
    FOLLOWER_DETAILS_TABLE_NAME

Base = declarative_base()


class UserDetails(Base):
    __tablename__ = USER_DETAILS_TABLE_NAME
    user_id = Column('user_id', BigInteger, index=True, nullable=False, unique=True)
    user_name = Column('user_name', String, primary_key=True)
    followers = Column('followers', Integer, default=0)
    following = Column('following', Integer, default=0)
    tweets = Column('tweets', Integer, default=0)
    created_at = Column('created_at', DateTime)

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['{}.user_id'.format(USER_TABLE_NAME)],
                             name='{}_user_id_{}_user_id_f_key'.format(USER_DETAILS_TABLE_NAME, USER_TABLE_NAME)),
    )


class TweetDetails(Base):
    __tablename__ = TWEET_DETAILS_TABLE_NAME
    tweet_id = Column('tweet_id', BigInteger, primary_key=True, autoincrement=True)
    tweet_msg = Column('tweet_msg', String, nullable=False)
    user_name = Column('user_name', String, nullable=False, index=True)
    twitted_at = Column('twitted_at', DateTime, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['user_name'], ['{}.user_name'.format(USER_DETAILS_TABLE_NAME)],
                             name='{}_user_name_{}_user_name_f_key'.format(TWEET_DETAILS_TABLE_NAME,
                                                                           USER_DETAILS_TABLE_NAME)),
    )


class FollowerDetails(Base):
    __tablename__ = FOLLOWER_DETAILS_TABLE_NAME
    user_name = Column('user_name', String, nullable=False, index=True)
    following_name = Column('following_name', String, nullable=False)
    followed_at = Column('followed_at', DateTime, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_name', 'following_name', name='{}_user_name_follower_name_primary_key'
                             .format(FOLLOWER_DETAILS_TABLE_NAME)),
        ForeignKeyConstraint(['user_name'], ['{}.user_name'.format(USER_DETAILS_TABLE_NAME)],
                             name='{}_user_name_{}_user_name_f_key'.format(FOLLOWER_DETAILS_TABLE_NAME,
                                                                           USER_DETAILS_TABLE_NAME)),
        ForeignKeyConstraint(['following_name'], ['{}.user_name'.format(USER_DETAILS_TABLE_NAME)],
                             name='{}_following_name_{}_user_name_f_key'.format(FOLLOWER_DETAILS_TABLE_NAME,
                                                                                USER_DETAILS_TABLE_NAME)),
    )


class User(Base):
    __tablename__ = USER_TABLE_NAME
    user_id = Column('user_id', BigInteger, primary_key=True, autoincrement=True)
    user_name = Column('user_name', String, nullable=False, unique=True, index=True)
    password = Column('password', String, nullable=False)
