import os

from bottle import Bottle, run, route, template, static_file, request, get


def home_page():
    client_ip = request.environ.get('REMOTE_ADDR')
    return template('./static/home')

def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        return "Success"
    else:
        return template('./static/register')

def about():
    return static_file("index.html", root='./static')

def project_page():
    return template('./static/projects')

def contact_page():
    return template('./static/contact')

@route('/server/<filename>')
def server_style(filename):
    return static_file(filename, root='./style')


def create_app():
    app = Bottle()
    app.route("/", "GET", home_page)
    app.route("/register", "GET", register)
    app.route("/overview", "GET", about)
    app.route("/projects", "GET", project_page)
    app.route("/contact", "GET", contact_page)

    return app



if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
