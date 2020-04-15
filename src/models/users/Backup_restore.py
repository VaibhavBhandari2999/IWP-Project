import datetime
import os
import shutil
import subprocess
import uuid
from src.common.utils1 import Utils

class Backup_restore(object):
    def __init__(self,date=None,_id=None):
        self.date = date if date is not None else datetime.datetime.strftime(Utils.current_time(),"%d-%m-%Y")
        self._id = uuid.uuid4().hex if _id is None else _id


    def restore(self):
        x = open("C:\\Users\\Dell\\Desktop\\third.bat")
        old = x.read()
        x.close()
        x = open("C:\\Users\\Dell\\Desktop\\third.bat", 'w')
        # old = x.read()
        x.write("mongorestore --db office_test_1 --drop C:\\Users\\Dell\\Desktop\\Projects\\Invoices\\backup\\" + self.date + "\\office_test_1")
        x.close()
        subprocess.call([r'C:\Users\Dell\Desktop\third.bat'])
        x = open("C:\\Users\\Dell\\Desktop\\third.bat", 'w')
        # old = x.read()
        x.write(old)
        x.close()

    @staticmethod
    def backup():
        try:
            os.mkdir("C:\\Users\\Dell\\Desktop\\Projects\\Invoices\\backup")
        except:
            print("Directory Exist")

        z = datetime.datetime.strftime(Utils.current_time(), "%d-%m-%Y")
        if os.path.exists("C:\\Users\\Dell\\Desktop\\Projects\\Invoices\\backup\\" + z):
            shutil.rmtree("C:\\Users\\Dell\\Desktop\\Projects\\Invoices\\backup\\" + z)
            print("ok")
        f = open("C:\\Users\\Dell\\Desktop\\second.bat", 'w')

        f.write("mongodump --db office_test_1 --out C:\\Users\\Dell\\Desktop\\Projects\\Invoices\\backup\\" + z)
        f.close()
        subprocess.call([r'C:\Users\Dell\Desktop\second.bat'])

        x = open("C:\\Users\\Dell\\Desktop\\third.bat", 'w')
        # old = x.read()
        x.write("mongorestore --db office_test_1 --drop C:\\Users\\Dell\\Desktop\\Projects\\Invoices\\backup\\" + z + "\\office_test_1")
        x.close()

