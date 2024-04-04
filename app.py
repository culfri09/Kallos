import logging
from flask import Flask, request

app = Flask(__name__)

# Define a route 
@app.route('/')
def init():
    return 'This is an HTTPS site'

# Run Flask application
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='localhost', port=8443)