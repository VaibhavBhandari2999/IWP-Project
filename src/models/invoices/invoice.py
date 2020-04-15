from src.common.database import Database
import uuid
import src.models.invoices.constants as InvoiceConstants
import datetime
from src.common.utils1 import Utils
from src.models.invoices.invoice_item import Invoice_item
from src.models.items.item import Item
from src.models.parties.party import Party

import src.models.parties.constants as PartyConstants

import src.models.items.constants as ItemConstants

from src.models.invoices.serial_no import Serial_no

class Invoice(object):
    def __init__(self, no, party_id, total_amount, date=None, narration=None, e_way=None,_id=None):
        self.no = no
        self.party_id = party_id
        if type(date) is not datetime.datetime:
            print("inside")
            self.date = Utils.current_time() if date is None else datetime.datetime.strptime(date,"%d-%m-%Y")
        else:
            print("outside")
            self.date =date
        self._id = uuid.uuid4().hex if _id is None else _id
        self.narration = narration
        self.total_amount = total_amount
        self.e_way = e_way

    def save_to_mongo(self):
        Database.update(InvoiceConstants.INVOICE_COLLECTION,{"_id":self._id},self.json())

    def json(self):
        return {
            "no" : self.no,
            "party_id" : self.party_id,
            "date" :self.date,
            "_id" : self._id,
            "narration" : self.narration,
            "total_amount":self.total_amount,
            "e_way":self.e_way
        }

    @classmethod
    def get_all_invoice(cls):
        return [cls(**elm) for elm in Database.find(InvoiceConstants.INVOICE_COLLECTION,{})]

    @classmethod
    def get_by_id(cls,id):
        return cls(**Database.find_one(InvoiceConstants.INVOICE_COLLECTION,{"_id":id}))

    def delete(self):
        Invoice_item.delete_by_invoice_id(self._id)
        Database.delete(InvoiceConstants.INVOICE_COLLECTION,{"_id":self._id})

    @staticmethod
    def get_data_for_list():
        json_datas = []
        invoices = Invoice.get_all_invoice()
        for invoice in invoices:
            invoice.party_id = Party.get_by_id(invoice.party_id)
            x = "<td><div class=\"dropdown-content\"><a id=\"navbarDropdownMenuLink"+invoice._id+"\" href=\"#\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\" class=\"nav-link tasks-toggle\"><i class=\"icon-new-file\"></i></a><div aria-labelledby=\"navbarDropdownMenuLink"+invoice._id+"\" class=\"invoice_datatable dropdown-menu tasks-list\"><a href=\"/invoices/edit/"+invoice._id+"\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-pencil fa-fw\"></i>  Edit</strong></div></a><a     data-href=\"/invoices/delete/"+invoice._id+"\" data-toggle=\"modal\" data-target=\"#confirm-delete\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-trash-o fa-fw\"></i>  Delete</strong></div></a><a href=\"/invoices/print/"+invoice._id+"\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-file-pdf-o fa fw\" style=\"margin-right: 6px;padding-left: 3px;\"></i>  Print</strong></div></a></div></div></td>"

            json_data = {
                "no" : str(invoice.no),
                "date" : datetime.datetime.strftime(invoice.date,"%d-%m-%Y"),
                "party_ac_name":invoice.party_id.name,
                "party_city":invoice.party_id.city,
                "total_amount":invoice.total_amount,
                "party_contact_person_name": invoice.party_id.contact_person,
                "party_contact":invoice.party_id.mobile_no_1,
                "actions" : x,
            }
            json_datas.append(json_data)
        #print(json_datas)
        return json_datas

    @staticmethod
    def get_data_for_serial_no_list():
        json_datas = []
        serial_nos = Serial_no.get_all_serial_no()
        for serial_no in serial_nos:
            invoice_item = Invoice_item.get_by_id(serial_no.invoice_item_id)
            invoice_item.item_id = Item.get_by_id(invoice_item.item_id)
            invoice = Invoice.get_by_id(invoice_item.invoice_id)
            invoice.party_id = Party.get_by_id(invoice.party_id)
            x = "<td><div class=\"dropdown-content\"><a id=\"navbarDropdownMenuLink"+invoice._id+"\" href=\"#\" data-toggle=\"dropdown\"aria-haspopup=\"true\" aria-expanded=\"false\" class=\"nav-link tasks-toggle\"><i class=\"icon-new-file\"></i></a><div aria-labelledby=\"navbarDropdownMenuLink"+invoice._id+"\" class=\"invoice_datatable dropdown-menu tasks-list\"><a href=\"/invoices/print/"+invoice._id+"\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-file-pdf-o fa fw\" style=\"margin-right: 6px;padding-left: 3px;\"></i>Print</strong></div></a></div></div></td>"

            json_data = {
                "no" : serial_no.serial_no,
                "invoice_no" : invoice.no,
                "date" : datetime.datetime.strftime(invoice.date,"%d-%m-%y"),
                "item" : invoice_item.item_id.model_name,
                "party" : invoice.party_id.name,
                "city": invoice.party_id.city,
                "price" : invoice_item.rate_per,
                "action" : x,
            }
            json_datas.append(json_data)
        return json_datas

    def get_all_invoice_item(self):
        return Invoice_item.get_by_invoice_id(self._id)

    @staticmethod
    def delete_item_possible(item_id):
        j = 0
        invoices = Invoice.get_all_invoice()
        for invoice in invoices:
            invoice_items = invoice.get_all_invoice_item()
            for invoice_item in invoice_items:
                if invoice_item.item_id == item_id:
                    j = 1
                    break
            if j == 1:
                break

        if j == 0:
            Database.delete(ItemConstants.ITEM_COLLECTION, {"_id": item_id})
            return True
        else:
            return "Item already exists in Invoice it Cannot be Deleted <br>However if you want to delete this data you can first delete all the linked invoices"


    @staticmethod
    def delete_party_possible(party_id):
        invoices = Invoice.get_all_invoice()
        for invoice in invoices:
            if invoice.party_id == party_id:
                 break

            Database.delete(PartyConstants.PARTY_COLLECTION, {"_id": party_id})
            return True
        else:
            return "This Party already exists in Invoice it Cannot be Deleted <br>However if you want to delete this data you can first delete all the linked invoices"


    @classmethod
    def filter_by_date(cls,start,end):
        invoice =  [cls(**elm) for elm in Database.find(InvoiceConstants.INVOICE_COLLECTION,
                                                    {'date': {'$lt': end, '$gte': start}})]
        #print(invoice)
        return invoice

    @staticmethod
    def count_invoices():
        return Database.count_documents(InvoiceConstants.INVOICE_COLLECTION,{})