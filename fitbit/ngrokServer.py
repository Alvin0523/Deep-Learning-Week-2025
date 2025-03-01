from flask import Flask, request

# DO NOT DELETE WE NEED TO BOOTSTRAP THE SERVER TO RUN
app = Flask(__name__)

@app.route('/')
def oauth_callback():
    # Retrieve the 'code' query parameter from the URL
    auth_code = request.args.get('code')
    if auth_code:
        # Print or save the authorization code as needed
        print("Received Authorization Code:", auth_code)
        return """
            <html>
                <head><title>Authorization Successful</title></head>
                <body>
                    <h1>Authorization Successful</h1>
                    <p>You can now close this window.</p>
                </body>
            </html>
            """
    else:
        return """
            <html>
                <head><title>Error</title></head>
                <body>
                    <h1>No authorization code received.</h1>
                    <p>Please try again.</p>
                </body>
            </html>
            """

if __name__ == '__main__':
    # Run the server on port 8080
    app.run(host='0.0.0.0', port=8080)
