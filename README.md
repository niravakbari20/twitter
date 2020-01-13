# Twitter

Below are the functionalities of twitter:
   -   A user should be able to sign up / login
   -   Users should be able to follow each other
   -   User should be able to tweet about anything they like
   -   When a user comes on their homepage, they should see all the tweets of people they are following sorted by latest tweet on top

## Installation

Please install the attached requirements.txt file before running the program.

```bash
pip install -r requirements.txt
```

## Running
##### Pleas check the pg connection config in /src/conf/pg_conf.py before running
# 
```bash
python app.py
open http://0.0.0.0:5000/
```

## ToDo
- UTs
- Retry logic in all post requests
- Making the post_tweet, increasing counts for tweet, followers and following a celery task.
- User session caching in Redis with ttl logic for faster login experience
- 1 database with global users table and per user schema
