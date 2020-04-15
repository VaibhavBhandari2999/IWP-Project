from src.common.database import Database
import uuid

import src.models.parties.constants as PartyConstants

class Contact_person_mobile(object):
    def __init__(self,mobile_no, contact_person_id,_id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.mobile_no = mobile_no
        self.contact_person_id = contact_person_id

    def save_to_mongo(self):
        Database.update(PartyConstants.CONTACT_PERSON_MOBILE_NO,{"_id":self._id}, self.json())

    def json(self):
        return {
            "_id" : self._id,
            "mobile_no" : self.mobile_no,
            "contact_person_id" : self.contact_person_id
        }



