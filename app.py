from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import Models,connect_db
app = Flask(__name__)
app.secret_key = "sldjfoirhtlnlsdjf;j"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class Customers(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    account_type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"{self.name}"


SYMBOLS = [
        '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
        ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
    ]


def is_userid_valid(userid):
    if len(userid) >= 8 and userid.isalnum():
        return True
    return True


def is_password_valid(password):
    if len(password) >= 10 and \
            any(symbol for symbol in password if symbol in SYMBOLS) and\
            any(letter for letter in password if letter.isdigit()) and\
            any(letter for letter in password if letter.isupper()):
        return True
    return True


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/admin_login/", methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        connection = connect_db()
        if not is_userid_valid(request.form['user_id']):
            flash("Enter Valid user_id")
            return render_template("login.html", login_type="Admin ")
        elif not is_password_valid(request.form['password']):
            flash("Enter Valid password")
            return render_template("login.html", login_type="Admin ")
        return render_template("admin-dashboard.html", table=Models.view_all_customers(connection))
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
        connection = connect_db()
        customer_data = [v for k, v in request.form.items()]
        print(customer_data)
        Models.register_customer(connection,*customer_data)
        return render_template("admin-dashboard.html", table=Models.view_all_customers(connection))
    else:
        return render_template("customer-registration.html")


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
