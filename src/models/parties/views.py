from flask import Blueprint, request, session, url_for, render_template, jsonify
from werkzeug.utils import redirect

from src.models.invoices.invoice import Invoice
from src.models.parties.party import Party
from src.models.users.user import User
import src.models.users.errors as UserErrors


import src.models.users.decorators as user_decorators


__author__="Vaibhav"

party_blueprint = Blueprint('parties',__name__)

@party_blueprint.route('/')
@user_decorators.requires_login
def index():
    return render_template("party/party_list.jinja2",datatable_page=True,party_list_page=True)

@party_blueprint.route('/new_party',methods=['GET','POST'])
@user_decorators.requires_login
def new_party():
    if request.method == 'POST':
        name = request.form.get('name')
        gstin = request.form.get('gstin')
        address = request.form.get('local_address')
        state = request.form.get('state')
        country = request.form.get('country')
        pincode =request.form.get('pincode')
        contact_person_name = request.form.get('contact_person_name')
        email = request.form.get('email')
        mobile_no_1 = request.form.get('mobile_no_1')
        mobile_no_2 = request.form.get('mobile_no_2')
        city = request.form.get('city')

        party = Party(name,gstin,address,city,state,country,int(pincode),contact_person_name,mobile_no_1,email,mobile_no_2)
        party.save_to_mongo()
        #f = request.form
        #print(f)
        #for key in f.keys():
        #    for value in f.getlist(key):
        #        print(key,value)

        return redirect(url_for('.index'))

    return render_template('party/new_party.jinja2',new_party_page=True)

@party_blueprint.route('/index_get_data')
@user_decorators.requires_login
def party_data():
    #Assume data comes from somewhere else
    data = {}
    data["data"] = Party.get_data_for_list()
    return jsonify(data)

@party_blueprint.route('/delete/<string:party_id>')
@user_decorators.requires_login
def delete_party(party_id):
    x = Invoice.delete_party_possible(party_id)
    if x==True:
        return redirect(url_for('.index'))
    else:
        return x



@party_blueprint.route('/edit/<string:party_id>',methods=['GET','POST'])
@user_decorators.requires_login
def edit_party(party_id):
    if request.method == 'POST':
        name = request.form.get('name')
        gstin = request.form.get('gstin')
        address = request.form.get('local_address')
        state = request.form.get('state')
        country = request.form.get('country')
        pincode = request.form.get('pincode')
        contact_person_name = request.form.get('contact_person_name')
        email = request.form.get('email')
        mobile_no_1 = request.form.get('mobile_no_1')
        mobile_no_2 = request.form.get('mobile_no_2')
        city = request.form.get('city')
        id = party_id

        party = Party(name, gstin, address, city, state, country, int(pincode), contact_person_name, mobile_no_1, email,
                      mobile_no_2,party_id)
        party.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('party/edit_party.jinja2',new_party_page=True,party= Party.get_by_id(party_id))