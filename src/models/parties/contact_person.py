from src.common.database import Database
import uuid

import src.models.parties.constants as PartyConstants

class Contact_person(object):
    def __init__(self, name, party_id, notes=None, _id=None):
        self.name = name
        self.notes = notes
        self._id = uuid.uuid4().hex if _id is None else _id
        self.party_id = party_id


    def save_to_mongo(self):
        Database.update(PartyConstants.CONTACT_PERSON_COLLECTION,{"_id":self._id},self.json())

    def json(self):
        return {
            "name" : self.name,
            "notes" : self.notes,
            "_id" : self._id,
            "part_id" : self._id
        }
