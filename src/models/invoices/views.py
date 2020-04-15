import datetime

from flask import Blueprint, request, session, url_for, render_template,jsonify
from werkzeug.utils import redirect

from src.models.companies.company import Company
from src.models.invoices.excel_sheet_maker import Excel_export
from src.models.invoices.invoice import Invoice
from src.models.invoices.invoice_item import Invoice_item
from src.models.invoices.serial_no import Serial_no
from src.models.items.item import Item
from src.common.utils1 import Utils
import src.models.users.decorators as user_decorators
from src.models.items.type import Type
from src.models.parties.party import Party

__author__="Vaibhav"

invoice_blueprint = Blueprint('invoices',__name__)


@invoice_blueprint.route('/')
@user_decorators.requires_login
def index():
    return render_template('invoices/invoice_list.jinja2',datatable_page=True,invoice_list_page=True)

@invoice_blueprint.route('/new',methods=['GET','POST'])
@user_decorators.requires_login
def new_invoice():
    print(session['email'])
    if request.method=='POST':
        string={}
        data = request.form
        print(data)
        print()
        for key in data.keys():
            for value in data.getlist(key):
                string[key]=value
        # ---- Invoice Creation ----

        no = string['number']
        party_id = Party.get_by_gstin(string['select_party'])

        date = string['date']
        narration = string['narration']

        invoice_amount=string['total_amount']
        e_way = string['e_way']

        invoice = Invoice(no,party_id._id,invoice_amount,date,narration,e_way)
        invoice.save_to_mongo()
        s = invoice._id
        print('invoice_id',s)
        # --- Find Items
        items = []
        serial_no = {}

        for i in string:
            print(i[:7])
            if i[:12] == 'select_item_':
                items.append([i, string[i][14::]])

            if i[:7] == 'myModal':
                if i[8] != '_':
                    num = int(i[7]) * 10 + int(i[8])
                else:
                    num = int(i[7])
                if str(num) not in serial_no:
                    serial_no[str(num)] = []

                serial_no[str(num)].append(string[i])

        #print(items)
        item_details = []
        for i in range(len(items)):
            item = items[i][0][12::]
            quantity = string['quantity_' + item]
            rate_per = string['rate_per_' + item]
            item_details.append([item,items[i][1], quantity, rate_per, serial_no[item]])

        #print()
        #print(item_details)

        for i in item_details:
            item_id = Item.get_by_name(i[1])
            print(invoice._id,item_id,float(i[3]),int(i[2]))
            invoice_item = Invoice_item(invoice._id,item_id._id,float(i[3]),int(i[2]))
            invoice_item.save_to_mongo()
            for j in i[4]:
                serial_no = Serial_no(invoice_item._id,j)
                serial_no.save_to_mongo()
        #print()
        #print(serial_no)
        #print(string)

        return redirect(url_for('.print_invoice',invoice_id=s))

    parties = Party.get_parties()
    items = Item.get_items()
    return render_template('invoices/new_invoice.jinja2',new_invoice_page=True,parties=parties,items=items,company=Company.get_company()[0])


@invoice_blueprint.route('/delete/<string:invoice_id>')
@user_decorators.requires_login
def delete_invoice(invoice_id):
    Invoice.get_by_id(invoice_id).delete()
    return redirect(url_for('.index'))


@invoice_blueprint.route('/edit/<string:invoice_id>',methods=['GET','POST'])
@user_decorators.requires_login
def edit_invoice(invoice_id):
    parties = Party.get_parties()
    items = Item.get_items()
    invoice_items = Invoice_item.get_by_invoice_id(invoice_id)

    company = Company.get_company()
    invoice = Invoice.get_by_id(invoice_id)
    invoice.date = datetime.datetime.strftime(invoice.date, "%d-%m-%Y")
    invoice_package = {}
    invoice_package['invoice'] = invoice

    party = Party.get_by_id(invoice.party_id)

    invoice_package['party'] = party
    tax_type = party.tax_type()
    tax, igst, round_off, total_amount, hsn_taxable_tot, total_quantity = 0.0, 0.0, 0.0, 0.0, 0.0, 0

    invoice_package['invoice_items'] = []
    sr = 0

    for invoice_item in invoice_items:
        sr += 1
        serial_no = Serial_no.get_by_invoice_item_id(invoice_item._id)
        total_quantity += invoice_item.quantity
        item = Item.get_by_id(invoice_item.item_id)
        amount_item = int(invoice_item.quantity) * float(invoice_item.rate_per)
        if tax_type == "gst":
            tax1 = amount_item * float(item.tax) / 200
            total_amount += (tax1 * 2)
        else:
            tax1 = amount_item * float(item.tax) / 100
            total_amount += tax1
        tax += tax1
        hsn_taxable_tot += amount_item
        invoice_package['invoice_items'].append({
            "invoice_item": invoice_item,
            "item": item,
            "serial_no": serial_no,
            "amount": amount_item,
            "sr_no": sr
        })

    if tax_type == "gst":
        x = tax * 2
    else:
        x = tax
    invoice_package['total_tax_amount'] = x
    total = hsn_taxable_tot + x
    round_off = abs(round(total) - total)
    invoice_package['tax'] = tax
    invoice_package['total_items'] = len(invoice_items)
    invoice_package['round_off'] = round_off
    invoice_package['total'] = total
    invoice_package['tax_type'] = tax_type
    invoice_package['company'] = company[0]

    #    for i in invoice_package:
    #        print(i,invoice_package[i])

    if request.method == 'POST':
        Invoice.get_by_id(invoice_id).delete()
        string = {}
        data = request.form
        print(data)
        print()
        for key in data.keys():
            for value in data.getlist(key):
                string[key] = value

        for i in string:
            print(i,string[i])
        # ---- Invoice Creation ----

        no = string['number']
        party_id = Party.get_by_gstin(string['select_party'])

        date = string['date']
        narration = string['narration']

        invoice_amount = string['total_amount']
        e_way = string['e_way']

        invoice = Invoice(no, party_id._id, invoice_amount, date, narration,e_way)
        invoice.save_to_mongo()
        # --- Find Items
        items = []
        serial_no = {}

        for i in string:
            print(i[:7])
            if i[:12] == 'select_item_':
                items.append([i, string[i][14::]])

            if i[:7] == 'myModal':
                if i[8] != '_':
                    num = int(i[7]) * 10 + int(i[8])
                else:
                    num = int(i[7])
                if str(num) not in serial_no:
                    serial_no[str(num)] = []

                serial_no[str(num)].append(string[i])

        # print(items)
        item_details = []
        for i in range(len(items)):
            item = items[i][0][12::]
            quantity = string['quantity_' + item]
            rate_per = string['rate_per_' + item]
            item_details.append([item, items[i][1], quantity, rate_per, serial_no[item]])

        # print()
        # print(item_details)

        for i in item_details:
            item_id = Item.get_by_name(i[1])
            print(invoice._id, item_id, float(i[3]), int(i[2]))
            invoice_item = Invoice_item(invoice._id, item_id._id, float(i[3]), int(i[2]))
            invoice_item.save_to_mongo()
            for j in i[4]:
                serial_no = Serial_no(invoice_item._id, j)
                serial_no.save_to_mongo()
        # print()
        # print(serial_no)
        # print(string)

        return redirect(url_for('.print_invoice', invoice_id=invoice._id))

    return render_template('invoices/edit_invoice.jinja2',invoice_package=invoice_package,edit_invoice_page=True,parties=parties,items=items,company=Company.get_company()[0])





@invoice_blueprint.route('/print/<string:invoice_id>')
@user_decorators.requires_login
def print_invoice(invoice_id):
    print(invoice_id)
    company = Company.get_company()
    company[0].address = format(company[0].address)
    company[0].address=Utils.format_address(company[0].address)

    invoice = Invoice.get_by_id(invoice_id)
    invoice.date = datetime.datetime.strftime(invoice.date,"%d-%m-%Y")
    invoice_items = Invoice_item.get_by_invoice_id(invoice_id)
    invoice_package = {}
    invoice_package['invoice'] = invoice
    #invoice_package.append(invoice)
    party = Party.get_by_id(invoice.party_id)
    party.address = Utils.format_address(party.address)
    invoice_package['party'] = party
    tax_type = party.tax_type()
    tax, igst, round_off, total_amount, hsn_taxable_tot, total_quantity = 0.0, 0.0, 0.0, 0.0, 0.0,0
    hsn_list = {}
    invoice_package['invoice_items'] = []
    sr=0
    for invoice_item in invoice_items:
        sr+=1
        serial_no = Serial_no.get_by_invoice_item_id(invoice_item._id)
        total_quantity += invoice_item.quantity
        #invoice_package.append([invoice_item,serial_no])

        item = Item.get_by_id(invoice_item.item_id)
        print(item.type_id)
        amount_item = int(invoice_item.quantity)*float(invoice_item.rate_per)

        if item.hsn not in hsn_list:
            hsn_list[item.hsn] = [0,invoice_item.rate_per,0,0,item.tax]

        if tax_type == "gst":
            tax1 = amount_item*float(item.tax)/200
            total_amount+=(tax1*2)
        else:
            tax1 = amount_item*float(item.tax)/100
            total_amount+=tax1

        hsn_list[item.hsn][2] += tax1
        hsn_list[item.hsn][0]+=amount_item

        if tax_type=="gst":
            hsn_list[item.hsn][3] += tax1*2
        else:
            hsn_list[item.hsn][3] += tax1
        hsn_taxable_tot +=amount_item
        tax += tax1

        print('Type_obj', item.type_id)
        item.type_id = Type.get_by_id(item.type_id)

        print(item.type_id)
        print()
        invoice_package['invoice_items'].append({
            "invoice_item":invoice_item,
            "item":item,
            "serial_no":serial_no,
            "amount":amount_item,
            "sr_no":sr
            })
    if tax_type == "gst":
        x = tax * 2
    else:
        x = tax
    invoice_package['total_tax_amount']=x
    total = hsn_taxable_tot+x
    round_off = abs(round(total)-total)

    invoice_package['hsn_taxable_total']=hsn_taxable_tot
    invoice_package['tax'] = tax
    invoice_package['total_items'] = len(invoice_items)
    invoice_package['round_off'] = round_off
    invoice_package['total'] = total
    invoice_package['tax_type'] = tax_type
    invoice_package['company'] = company[0]
    invoice_package['total_words'] = Utils.get_currency_words(total)
    if tax_type=="gst":
        invoice_package['tax_words'] = Utils.get_currency_words(tax*2)
    else:
        invoice_package['tax_words'] = Utils.get_currency_words(tax)
    invoice_package['hsn_list'] = hsn_list
    invoice_package['total_quantity'] = total_quantity
    #for i in invoice_package:
     #   print(i,invoice_package[i])

    #print()

    #for i in invoice_package['invoice_items']:
    #    print(i)

    print(invoice_package['hsn_list'])
    #print(company[0].address)
    #print(party.address)
    return render_template('invoices/invoice_print.jinja2',invoice_package=invoice_package)



@invoice_blueprint.route('/index_get_data')
@user_decorators.requires_login
def invoice_data():
    #Assume data comes from somewhere else
    data = {}
    data["data"] = Invoice.get_data_for_list()
    return jsonify(data)

@invoice_blueprint.route('/export',methods=['POST'])
@user_decorators.requires_login
def export():
    start = request.form.get('start_date')
    end = request.form.get('end_date')
    Excel_export(start,end).make_final_workbook()
    return redirect(url_for('.index'))

@invoice_blueprint.route('/serial_no')
@user_decorators.requires_login
def serial_no_datatable():
    return render_template('invoices/serial_no_list.jinja2',datatable_page=True,serial_no_list_page=True)


@invoice_blueprint.route('/serial_no_get_data')
@user_decorators.requires_login
def serial_no_data():
    #Assume data comes from somewhere else
    data = {}
    data["data"] = Invoice.get_data_for_serial_no_list()
    return jsonify(data)
