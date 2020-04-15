import uuid

from src.common.database import Database
import src.models.parties.constants as PartyConstants
from src.models.companies.company import Company


class Party(object):
    def __init__(self, name, gstin, address, city, state, country, pincode, contact_person, mobile_no_1=None, email=None, mobile_no_2=None, _id=None):
        self.name = name
        self.gstin = gstin
        self.address = address
        self.state = state
        self.country = country
        self.contact_person = contact_person
        self.email = email
        self.mobile_no_1 = mobile_no_1
        self.mobile_no_2 = mobile_no_2
        self.picode = pincode
        self._id = uuid.uuid4().hex if _id is None else _id
        self.city = city

    def save_to_mongo(self):
        Database.update(PartyConstants.PARTY_COLLECTION,{"_id" : self._id},self.json())

    def json(self):
        return {
            "_id" : self._id,
            "name" : self.name,
            "gstin" : self.gstin,
            "address" : self.address,
            "state" : self.state,
            "country" : self.country,
            "pincode" : self.picode,
            "contact_person" : self.contact_person,
            "email" : self.email,
            "mobile_no_1" : self.mobile_no_1,
            "mobile_no_2" : self.mobile_no_2,
            "city":self.city
        }

    @classmethod
    def get_parties(cls):
        return [cls(**elm) for elm in Database.find(PartyConstants.PARTY_COLLECTION,{})]

    @classmethod
    def get_by_gstin(cls,gstin):
        return cls(**Database.find_one(PartyConstants.PARTY_COLLECTION,{'gstin':gstin}))

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(PartyConstants.PARTY_COLLECTION, {'_id': id}))


    def tax_type(self):
        company = Company.get_company()
        #party = Party.get_by_id(id)
        if self.gstin[:2] == company[0].gstin[:2]:
            return 'gst'
        else:
            return 'igst'


    @staticmethod
    def get_data_for_list():
        json_datas = []
        parties = Party.get_parties()
        for party in parties:

            x = "<td><div class=\"dropdown-content\"><a id=\"navbarDropdownMenuLink"+party._id+"\" href=\"#\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\" class=\"nav-link tasks-toggle\"><i class=\"icon-new-file\"></i></a><div aria-labelledby=\"navbarDropdownMenuLink"+party._id+"\" class=\"invoice_datatable dropdown-menu tasks-list\"><a href=\"/parties/edit/"+party._id+"\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-pencil fa-fw\"></i>  Edit</strong></div></a><a     data-href=\"/parties/delete/"+party._id+"\" data-toggle=\"modal\" data-target=\"#confirm-delete\" class=\"dropdown-item\"><div class=\"text d-flex justify-content-between\"><strong><i class=\"fa fa-trash-o fa-fw\"></i>  Delete</strong></div></a></div></div></td>"

            json_data = {
                "name" : party.name,
                "city" : party.city,
                "gstin":party.gstin,
                "contact_person_name":party.contact_person,
                "mobile_no":party.mobile_no_1,
                "email": party.email,
                "actions" : x,
            }
            json_datas.append(json_data)
        print(json_datas)
        return json_datas

    @staticmethod
    def count_parties():
        return Database.count_documents(PartyConstants.PARTY_COLLECTION, {})
    """
    Party Delete is in invoice
    """

