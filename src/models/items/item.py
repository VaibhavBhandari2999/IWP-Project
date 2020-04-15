from src.common.database import Database
import uuid

#from src.models.invoices.invoice import Invoice
#from src.models.invoices.invoice_item import Invoice_item
from src.models.items.item_company import Item_company
import src.models.items.constants as ItemConstants
from src.models.items.type import Type


class Item(object):
    def __init__(self, hsn, company_id, model_name, type_id, tax, price, _id=None):
        self.hsn = hsn
        self.company_id  = Item_company.id_for_item(company_id)._id
        self.model_name = model_name
        self.type_id = Type.get_by_name_for_item(type_id)._id
        self.tax = tax
        self.price = price
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update(ItemConstants.ITEM_COLLECTION,{"_id":self._id},self.json())



    def json(self):
        return {
            "_id" : self._id,
            "hsn" : self.hsn,
            "company_id" : self.company_id,
            "model_name" : self.model_name,
            "type_id" : self.type_id,
            "tax" : self.tax,
            "price" : self.price,
        }

    @classmethod
    def get_items(cls):
        return [cls(**elm) for elm in Database.find(ItemConstants.ITEM_COLLECTION,{})]

    @classmethod
    def get_by_name(cls,name):
        return cls(**Database.find_one(ItemConstants.ITEM_COLLECTION,{"model_name":name}))

    @classmethod
    def get_by_id(cls,id):
        return cls(**Database.find_one(ItemConstants.ITEM_COLLECTION,{"_id":id}))


    @staticmethod
    def get_data_for_list():
        json_datas = []
        items = Item.get_items()
        for item in items:
            item.company_id = Item_company.find_by_id(item.company_id)
            item.type_id = Type.get_by_id(item.type_id)
            x = "<td><div class=\"dropdown-content\"><a id=\"navbarDropdownMenuLink"+item._id+"\" href=\"#\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\" class=\"nav-link tasks-toggle\"><i class=\"icon-new-file\"></i></a><div aria-labelledby=\"navbarDropdownMenuLink"+item._id+"\" class=\"invoice_datatable dropdown-menu tasks-list\"><a href=\"/items/edit/"+item._id+"\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-pencil fa-fw\"></i>  Edit</strong></div></a><a     data-href=\"/items/delete/"+item._id+"\" data-toggle=\"modal\" data-target=\"#confirm-delete\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-trash-o fa-fw\"></i>  Delete</strong></div></a></div></div></td>"

            json_data = {
                "model_name" : item.model_name,
                "company" : item.company_id.name,
                "hsn":item.hsn,
                "item_type":item.type_id.type_name,
                "tax":item.tax,
                "price": item.price,
                "actions" : x,
            }
            json_datas.append(json_data)
        #print(json_datas)
        return json_datas

    @staticmethod
    def count_items():
        return Database.count_documents(ItemConstants.ITEM_COLLECTION, {})

"""
Here delete is invoked from invoices
"""