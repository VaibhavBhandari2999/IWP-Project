from src.common.database import Database
import uuid
import src.models.items.constants as ItemConstants

class Item_company(object):
    def __init__(self, name,_id=None):
        self.name = name
        self._id  = uuid.uuid4().hex if _id is None else _id


    def save_to_mongo(self):
        Database.insert(ItemConstants.ITEM_COMPANY_COLLECTION,self.json())

    def json(self):
        return {
            "_id" : self._id,
            "name" : self.name
        }

    @classmethod
    def find_by_name(cls,name):
        return cls(**Database.find_one(ItemConstants.ITEM_COMPANY_COLLECTION, {"name":name}))

    @classmethod
    def find_by_id(cls,_id):
        return cls(**Database.find_one(ItemConstants.ITEM_COMPANY_COLLECTION,{"_id":_id}))


    @classmethod
    def id_for_item(cls,name):
        company = Database.find_one(ItemConstants.ITEM_COMPANY_COLLECTION, {"name":name})

        if company is None:
            company = Database.find_one(ItemConstants.ITEM_COMPANY_COLLECTION,{"_id": name})
            if company is None:
                company = Item_company(name)
                company.save_to_mongo()
            else:
                return cls(**company)
        else:
            company = cls(**company)

        print(company)
        return company

    @classmethod
    def get_all_companies(cls):
        return [cls(**elm) for elm in Database.find(ItemConstants.ITEM_COMPANY_COLLECTION,{})]

