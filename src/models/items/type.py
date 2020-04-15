import uuid

from src.common.database import Database
import src.models.items.constants as ItemConstants

class Type(object):
    def __init__(self,type_name,_id=None):
        self.type_name = type_name
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(ItemConstants.TYPE_COLLECTION,self.json())

    def json(self):
        return {
            "type_name" : self.type_name,
            "_id" : self._id
        }

    @classmethod
    def get_by_name_for_item(cls,name):
        type = Database.find_one(ItemConstants.TYPE_COLLECTION,{"type_name":name})
        if type is None:
            type = Database.find_one(ItemConstants.TYPE_COLLECTION,{"_id":name})
            if type is None:
                type = Type(name)
                type.save_to_mongo()
            else:
                return cls(**type)
        else:
            type = cls(**type)
        return type

    @classmethod
    def get_all_types(cls):
        return [cls(**elm) for elm in Database.find(ItemConstants.TYPE_COLLECTION,{})]

    @classmethod
    def get_by_id(cls,id):
        return cls(**Database.find_one(ItemConstants.TYPE_COLLECTION,{"_id":id}))
