import os
import pandas as pd
from bottle import Bottle, run, route, template, static_file, request, get
from hashlib import sha256
from find_pulsars import pulsar_classifier

def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()

def ip_handler():
    client_ip = request.environ.get('REMOTE_ADDR')
    ip_data = pd.read_csv('./data/ip_address.csv')
    new_ip_list = [client_ip, 1]
    for item in new_ip_list:
        print(item)
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

    user_data = pd.read_csv('./data/users.csv')
    
    if user_data.empty:
        user_data = pd.DataFrame([[username, email, password]], columns=['USERNAME','EMAIL','PASSWORD'])
    else:
        filtering = user_data['USERNAME'] == username
        if user_data[filtering].empty:
            add = pd.DataFrame([[username, email, password]], columns=['USERNAME','EMAIL','PASSWORD'])
            user_data = user_data.append(add, ignore_index=True)
        else:
            return "This username exists."

    user_data.to_csv('./data/users.csv', index = False)
    print(username,email,password)
    return "Success"


def about():
    return static_file("index.html", root='./static')

def project_page():
    return static_file("projects.html", root='./static')

def demo_input_page():
    return static_file("demo.html", root='./static')


def create_mlrequest():
    selected_model = request.forms.get('model')
    if selected_model=='clf':
        results, data, legend = pulsar_classifier()
        
        f = open("./static/demoresult.html", "r")
        html = f.read().format(score=results['score'], output1=results['feature'], datatable=data, legendtable=legend)
        return html
    if selected_model=='reg':
        results = pulsar_classifier()
        return results
    if selected_model=='clu':
        results = pulsar_classifier()
        return results
#<img src="/server/plot.png" id="plot" alt="plot">



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
    #Sidenav Options
    app.route("/", "GET", about)
    app.route("/projects", "GET", project_page)
    app.route("/demo", "GET", demo_input_page)

    #User inputs for models
    app.route("/demo", "POST", create_mlrequest)

    #Include style and images
    app.route("/server/index.css", "GET", get_style)
    app.route("/server/ai.png", "GET", get_banner)
    app.route("/server/pp.png", "GET", get_profile)
    app.route("/server/itulogo.jpg", "GET", get_uni)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
