from src.common.database import Database
import uuid

import src.models.invoices.constants as InvoiceConstants
from src.models.invoices.serial_no import Serial_no
from src.models.items.item import Item


class Invoice_item(object):
    def __init__(self, invoice_id ,item_id, rate_per,quantity, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.item_id = item_id
        self.rate_per = rate_per
        self.invoice_id = invoice_id
        self.quantity = quantity

    def save_to_mongo(self):
        Database.update(InvoiceConstants.INVOICE_ITEM_COLLECTION,{'_id':self._id},self.json())

    def json(self):
        return {
            "_id" : self._id,
            "item_id" :self.item_id,
            "quantity" : self.quantity,
            "invoice_id" : self.invoice_id,
            "rate_per" : self.rate_per
        }

    @classmethod
    def get_by_invoice_id(cls,invoice_id):
        return [cls(**elm) for elm in Database.find(InvoiceConstants.INVOICE_ITEM_COLLECTION,{'invoice_id':invoice_id})]

    @classmethod
    def delete_by_invoice_id(cls,invoice_id):
        invoice_items = Invoice_item.get_by_invoice_id(invoice_id)
        for invoice_item in invoice_items:
            Serial_no.delete_by_invoice_item_id(invoice_item._id)
            invoice_item.delete()

    def delete(self):
        Database.delete(InvoiceConstants.INVOICE_ITEM_COLLECTION,{"_id":self._id})

    @classmethod
    def get_by_id(cls,id):
        return cls(**Database.find_one(InvoiceConstants.INVOICE_ITEM_COLLECTION,{"_id":id}))
