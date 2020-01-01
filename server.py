import os
import pandas as pd
from bottle import Bottle, run, route, template, static_file, request, get
from hashlib import sha256

def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()

def home_page():
    client_ip = request.environ.get('REMOTE_ADDR')
    ip_data = pd.read_csv('ip_address.csv')
    
    if ip_data.empty:
        ip_data = pd.DataFrame([[client_ip, 1]], columns=['IP ADDRESS','COUNT'])
    else:
        filtering = ip_data['IP ADDRESS'] == client_ip
        if ip_data[filtering].empty:
            add = pd.DataFrame([[client_ip, 1]], columns=['IP ADDRESS','COUNT'])
            ip_data = ip_data.append(add, ignore_index=True)
        else:
            ip_data.loc[filtering,'COUNT'] += 1

    ip_data.to_csv('ip_address.csv', index = False)
    return ip_data.to_html()

def create_user():
    username = request.forms.get('username')
    email = request.forms.get('email')
    password = create_hash(request.forms.get('password'))

    user_data = pd.read_csv('users.csv')
    
    if user_data.empty:
        user_data = pd.DataFrame([[username, email, password]], columns=['USERNAME','EMAIL','PASSWORD'])
    else:
        filtering = user_data['USERNAME'] == username
        if user_data[filtering].empty:
            add = pd.DataFrame([[username, email, password]], columns=['USERNAME','EMAIL','PASSWORD'])
            user_data = user_data.append(add, ignore_index=True)
        else:
            return "This username exists."

    user_data.to_csv('users.csv', index = False)
    print(username,email,password)
    return "Success"


def register():
    return template('./static/register')

def about():
    return static_file("index.html", root='./static')

def project_page():
    return template('./static/projects')

def contact_page():
    return template('./static/contact')

@route('/static/<path:path>')
def server_static(path):
    print(os.getcwd() + '/static' + path)
    return static_file(path, root=os.getcwd() + '/static')

def get_style():
    return static_file("index.css", root='./static/style')
def get_banner():
    return static_file("ai.png", root='./static/style')
def get_profile():
    return static_file("pp.png", root='./static/style')
def get_uni():
    return static_file("itulogo.jpg", root='./static/style')


def create_app():
    app = Bottle()
    app.route("/", "GET", home_page)
    app.route("/register", "GET", register)
    app.route("/overview", "GET", about)
    app.route("/projects", "GET", project_page)
    app.route("/contact", "GET", contact_page)
    app.route("/create", "POST", create_user)
    app.route("/server/index.css", "GET", get_style)
    app.route("/server/ai.png", "GET", get_banner)
    app.route("/server/pp.png", "GET", get_profile)
    app.route("/server/itulogo.jpg", "GET", get_uni)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
