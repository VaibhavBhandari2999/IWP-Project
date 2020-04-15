from src.common.database import Database
import uuid

import src.models.invoices.constants as InvoiceConstants

class Serial_no(object):
    def __init__(self, invoice_item_id, serial_no, _id=None):
        self.invoice_item_id = invoice_item_id
        self.serial_no = serial_no
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update(InvoiceConstants.INVOICE_ITEM_SERIAL_NO,{"_id":self._id},self.json())

    def json(self):
        return {
            "serial_no" : self.serial_no,
            "_id" : self._id,
            "invoice_item_id" : self.invoice_item_id
        }
    @classmethod
    def get_by_invoice_item_id(cls,invoice_item_id):
        return [cls(**elm) for elm in Database.find(InvoiceConstants.INVOICE_ITEM_SERIAL_NO,{"invoice_item_id":invoice_item_id})]

    @classmethod
    def delete_by_invoice_item_id(cls,invoice_item_id):
        serial_nos = Serial_no.get_by_invoice_item_id(invoice_item_id)
        for serial_no in serial_nos:
            serial_no.delete()

    def delete(self):
        Database.delete(InvoiceConstants.INVOICE_ITEM_SERIAL_NO,{"_id":self._id})

    @classmethod
    def get_by_serial_no(cls,serial_no):
        Database.find(InvoiceConstants.INVOICE_ITEM_SERIAL_NO,{"serial_no":serial_no})

    @classmethod
    def get_all_serial_no(cls):
        return [cls(**elm) for elm in Database.find(InvoiceConstants.INVOICE_ITEM_SERIAL_NO,{})]


