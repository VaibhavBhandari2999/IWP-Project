from flask import Blueprint, request, render_template, redirect, url_for

from src.models.companies.company import Company


import src.models.users.decorators as user_decorators


__author__="Vaibhav"

company_blueprint = Blueprint('companies',__name__)

@company_blueprint.route('/',methods=['GET','POST'])
@user_decorators.requires_login
def index():
    companies = Company.get_company()
    if len(companies) == 0:
        if request.method=='POST':
            name = request.form.get('name')
            email = request.form.get('email')
            gstin = request.form.get('gstin')
            address = request.form.get('address')
            city = request.form.get('city')
            pincode = request.form.get('pincode')
            state = request.form.get('state')
            country = request.form.get('country')
            bank_name = request.form.get('bank_name')
            branch = request.form.get('branch')
            account_number = request.form.get('account_number')
            ifsc = request.form.get('ifsc')

            company = Company(name, gstin, address, city, state,pincode,email,bank_name,branch,ifsc,account_number)
            company.save_to_mongo()

            return redirect(url_for('users.index'))

        return render_template("company/add_company.jinja2",company_page=True)
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            gstin = request.form.get('gstin')
            address = request.form.get('address')
            city = request.form.get('city')
            pincode = request.form.get('pincode')
            state = request.form.get('state')
            country = request.form.get('country')
            bank_name = request.form.get('bank_name')
            branch = request.form.get('branch')
            account_number = request.form.get('account_number')
            ifsc = request.form.get('ifsc')
            print(state)
            company_edit = Company(name, gstin, address, city, state,pincode,email,bank_name,branch,ifsc,account_number,_id=companies[0]._id)
            company_edit.save_to_mongo()

            return redirect(url_for('users.index'))
        return render_template("company/edit_company.jinja2",company = companies[0], company_page = True)



