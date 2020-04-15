from flask import Blueprint, request, render_template, jsonify, redirect, url_for

from src.models.invoices.invoice import Invoice
from src.models.items.item_company import Item_company
from src.models.items.item import Item
from src.models.items.type import Type

import src.models.users.decorators as user_decorators


__author__="Vaibhav"

item_blueprint = Blueprint('items',__name__)

@item_blueprint.route('/')
@user_decorators.requires_login
def index():
    return render_template("items/item_list.jinja2",datatable_page=True,item_list_page=True)

@item_blueprint.route('/new',methods=['POST', 'GET'])
@user_decorators.requires_login
def new_item():
    if request.method == 'POST':
        print("POST")
        model_name = request.form.get('model_name')
        x = request.form.get('company_name')
        company = request.form.get('add_new_company')
        hsn_code = request.form.get('hsn_code')
        type = request.form.get('add_new_type')
        y = request.form.get('type')

        tax = request.form.get('tax')
        price = request.form.get('price')
        if company == None:
            company = x
        if type == None:
            type = y
        #print(model_name,x,company,hsn_code,type,y,tax,price)
        item = Item(hsn_code,company,model_name,type,tax,price)
        item.save_to_mongo()
        return redirect(url_for('.index'))
        #return render_template("KK")
    companies = Item_company.get_all_companies()
    types = Type.get_all_types()
    return render_template('items/new_item.jinja2',companies=companies,types=types,new_item_page=True)


@item_blueprint.route('/index_get_data')
@user_decorators.requires_login
def item_data():
    #Assume data comes from somewhere else
    data = {}
    data["data"] = Item.get_data_for_list()
    return jsonify(data)

@item_blueprint.route('/delete/<string:item_id>')
@user_decorators.requires_login
def delete_item(item_id):
    x = Invoice.delete_item_possible(item_id)
    if x==True:
        return redirect(url_for('.index'))
    else:
        return x


@item_blueprint.route('/edit/<string:item_id>',methods=['GET','POST'])
@user_decorators.requires_login
def edit_item(item_id):
    item = Item.get_by_id(item_id)
    companies = Item_company.get_all_companies()
    types = Type.get_all_types()

    if request.method=='POST':
        model_name = request.form.get('model_name')
        x = request.form.get('company_name')
        company = request.form.get('add_new_company')
        hsn_code = request.form.get('hsn_code')
        type = request.form.get('add_new_type')
        y = request.form.get('type')

        tax = request.form.get('tax')
        price = request.form.get('price')
        if company == None:
            company = x
        if type == None:
            type = y
        # print(model_name,x,company,hsn_code,type,y,tax,price)
        item = Item(hsn_code, company, model_name, type, tax, price,item_id)
        item.save_to_mongo()
        return redirect(url_for('.index'))

    return render_template('items/edit_item.jinja2',item=item,companies=companies,types=types,new_item_page=True)
