from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.models.invoices.invoice import Invoice
from src.models.items.item import Item
from src.models.parties.party import Party
from src.models.users.Backup_restore import Backup_restore
from src.models.users.user import User
import src.models.users.errors as UserErrors
__author__="Vaibhav"

import src.models.users.decorators as user_decorators
user_blueprint = Blueprint('users',__name__)

@user_blueprint.route('/')
@user_decorators.requires_login
def index():
    return render_template("users/index.jinja2",index_page=True,invoices_count = Invoice.count_invoices(),items_count = Item.count_items(), parties_count = Party.count_parties())

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == "POST":
        #Check Login is valid
        email = request.form['email']
        password= request.form['password']
        try:
            if User.is_login_valid(email,password):
                session['email'] = email
                return redirect(url_for('.index'))
        except UserErrors.UserError as e:
            return e.message

    return render_template("login.jinja2") #Send the User an error is needed if login is invalid

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        #Check Login is valid
        email = request.form['email']
        password= request.form['password']
        username = request.form['username']
        #print(email,password)
        try:
            if User.register_user(email,password,username):
                session['email'] = email
                return "This is for admin"
        except UserErrors.UserError as e:
            return e.message
    #print(session['email'])

    return render_template("register.jinja2") #Send the User an error is needed if login is invalid
    #return "Register page"

@user_blueprint.route('/logout')
def user_logout():
    session['email']=None
    return redirect(url_for('home'))
#.home redirects in the same blueprint

@user_blueprint.route('/backup',methods=["POST"])
def database():
    action_type = request.form.get('action_type')
    date = request.form.get('date')
    #print(date,action_type)
    x = Backup_restore(date)
    if action_type == "backup":
        Backup_restore.backup()
    else:
        x.restore()
    return redirect(url_for(".index"))
