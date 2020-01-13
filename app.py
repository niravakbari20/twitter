from os import environ
from src.resources.twitter_view import app

if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0', port=port)
