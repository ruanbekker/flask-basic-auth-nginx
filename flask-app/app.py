from flask import Flask, render_template
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

basic_auth = BasicAuth(app)

@app.route('/')
def main():
    return 'welcome'

@app.route('/secret')
@basic_auth.required
def secret_view():
    return 'authorized'

if '__main__' == __name__:
    app.run(host='0.0.0.0')
