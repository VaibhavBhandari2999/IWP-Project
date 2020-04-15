import uuid

from src.common.database import Database
from src.common.utils1 import Utils
import src.models.companies.constants as CompanyConstants
class Company(object):
    def __init__(self, name, gstin, address, city, state, pincode, email, bank_name, branch, ifsc, account_number, _id=None):
        self.name = name
        self.gstin = gstin
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.email = email
        self.bank_name = bank_name
        self.branch = branch
        self.ifsc = ifsc
        self.account_number = account_number
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update(CompanyConstants.COLLECTION,{"_id":self._id},self.json())

    def json(self):
        return {
            "name" : self.name,
            "gstin" : self.gstin,
            "address" : self.address,
            "city" : self.city,
            "state" : self.state,
            "pincode" : self.pincode,
            "email" : self.email,
            "bank_name" : self.bank_name,
            "branch" : self.branch,
            "ifsc" : self.ifsc,
            "account_number" : self.account_number,
            "_id" : self._id,
        }

    @classmethod
    def get_company(cls):
        companies = Database.find(CompanyConstants.COLLECTION,{})
        return [cls(**elm) for elm in companies]