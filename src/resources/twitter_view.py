from flask import Flask, render_template, request, session, jsonify

from src.services.twitter_services import validate_login_user, add_new_user, get_all_tweets, post_user_tweet, \
    add_follower

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello {}!  <a href='/logout'>Logout</a> <a href='/post_tweet'>Post Tweets</a> " \
               "<a href='/tweet'>Tweets</a> <a href='/follow'>Follow</a>"\
            .format(session.get('username'))


@app.route('/signup', methods=['GET'])
def get_signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():
    if not request.form['password'] or not request.form['username']:
        return 'Please enter all user data for signup'
    else:
        creation_resp = add_new_user(request.form['username'], request.form['password'])
        if creation_resp:
            return render_template('login.html')
        else:
            return 'Sign Up Failed'


@app.route('/login', methods=['POST'])
def login():
    if not request.form['password'] or not request.form['username']:
        return 'Please enter all user data for login'
    else:
        validation_response, msg = validate_login_user(request.form['username'], request.form['password'])
        if validation_response:
            session['logged_in'] = True
            session['username'] = request.form['username']
        else:
            return msg
        return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username')
    return home()


@app.route('/tweet', methods=['GET'])
def get_tweets():
    if session.get('logged_in'):
        tweets = get_all_tweets(session)
        if tweets:
            return jsonify(tweets)
        return 'No tweets for you please check later!'
    return home()


@app.route('/post_tweet', methods=['GET'])
def get_post_tweet():
    if session.get('logged_in'):
        return render_template('tweet.html')
    return home()


@app.route('/tweet', methods=['POST'])
def post_tweet():
    if session.get('logged_in'):
        msg, resp = post_user_tweet(session, request.form['tweet'])
        if resp == 200:
            return home()
        return msg
    return home()


@app.route('/follow', methods=['GET'])
def get_post_follower():
    if session.get('logged_in'):
        return render_template('follow.html')
    return home()


@app.route('/follow', methods=['POST'])
def post_follower():
    if session.get('logged_in'):
        msg, resp = add_follower(session, request.form['following'])
        if resp == 200:
            return home()
        return msg
    return home()
