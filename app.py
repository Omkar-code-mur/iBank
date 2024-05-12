from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "sldjfoirhtlnlsdjf;j"
SYMBOLS = [
        '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
        ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
    ]


def is_userid_valid(userid):
    if len(userid) >= 8 and userid.isalnum():
        return True
    return False


def is_password_valid(password):
    if len(password) >= 10 and \
            any(symbol for symbol in password if symbol in SYMBOLS) and\
            any(letter for letter in password if letter.isdigit()) and\
            any(letter for letter in password if letter.isupper()):
        return True
    return False


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/admin_login/", methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        if not is_userid_valid(request.form['user_id']):
            flash("Enter Valid user_id")
            return render_template("login.html", login_type="Admin ")
        elif not is_password_valid(request.form['password']):
            flash("Enter Valid password")
            return render_template("login.html", login_type="Admin ")
        return render_template("admin-dashboard.html")
    return render_template("login.html", login_type="Admin ")


@app.route("/customer_login/", methods=['GET', 'POST'])
def customer_login():
    if request.method == "POST":
        return render_template("customer-dashboard.html")
    return render_template("login.html", login_type="Customer ")


# @app.route("/admin_dashboard/", methods=['GET', 'POST'])
# def admin_dashboard():
#     if request.method == "POST":
#         return render_template("admin-dashboard.html")
#     else:
#         return render_template("login.html", login_type="Admin ")
#
#
# @app.route("/customer_dashboard/", methods=['GET', 'POST'])
# def customer_dashboard():
#     if request.method == "POST":
#         return render_template("customer-dashboard.html")
#     else:
#         return render_template("login.html", login_type="Customer ")


@app.route("/admin-logged-in/customer_registration/", methods=['GET', 'POST'])
def customer_registration():
    if request.method == "POST":
        return render_template("customer_registration.html")
    else:
        return "Invalid URL"


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/services/")
def services():
    return render_template("services.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(debug=True)