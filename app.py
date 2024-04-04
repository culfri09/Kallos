import logging
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='./template')

# Defines index.html as the root of the URL
@app.route('/')
def index():
    return render_template('register.html')

# Run Flask application
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='localhost', port=8443)