from src.common.database import Database
from src.config import Config

__author__= 'Vaibhav'
from flask import Flask, render_template, session,jsonify

app=Flask(__name__)

app.config.from_object(Config)
app.secret_key = "vaibhav"


@app.before_first_request
def init_db():
    session['email'] = None
    Database.initialize()

@app.route('/')
def home():
    session['email'] = None
    return render_template('home.jinja2')

from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint,url_prefix="/users")

from src.models.items.views import item_blueprint
app.register_blueprint(item_blueprint,url_prefix="/items")

from src.models.parties.views import party_blueprint
app.register_blueprint(party_blueprint,url_prefix="/parties")

from src.models.invoices.views import invoice_blueprint
app.register_blueprint(invoice_blueprint,url_prefix="/invoices")

from src.models.companies.views import company_blueprint
app.register_blueprint(company_blueprint,url_prefix="/companies")