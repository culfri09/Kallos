from website import init

# Create Flask application
app = init.create_app()

# Run Flask application
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='localhost', port=8443)

