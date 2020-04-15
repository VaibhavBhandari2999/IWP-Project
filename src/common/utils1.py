import re

from num2words import num2words
from passlib.hash import pbkdf2_sha512
import pytz
__author__ = "Vaibhav"

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pytz import timezone

class Utils(object):

    @staticmethod
    def send_email_msg(to_list, msg, subject, username, password):
        host = "smtp.gmail.com"
        port = 587
        # username = "hspecter1999@gmail.com"
        # password = "ironmanROCKS"

        obj = smtplib.SMTP(host, port)
        obj.ehlo()
        obj.starttls()
        obj.login(username, password)
        this_msg = MIMEMultipart("alternative")
        this_msg['Subject'] = subject
        this_msg['From'] = username
        this_msg['to'] = to_list
        plain_txt = msg
        part1 = MIMEText(plain_txt, 'plain')
        this_msg.attach(part1)
        try:
            obj.sendmail(username, [to_list], this_msg.as_string())
            print("Email Sent Succesfully")
        except:
            print("Unable to sent Email")

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)*[\w-]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from login/register form
        :return:A sha512->pbkdf2_sha512 encrypted password
        """

        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        #print(password, hashed_password)
        """
        Checks that the password the user sent matches that of the database
        The database password is more encrypted than user's password
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return True if password match, false otherwise
        """
        # x = pbkdf2_sha512.encrypt(password)
        # print(x)
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def current_time():

        format = "%Y-%m-%d %H:%M:%S %Z%z"
        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))
        #print(now_utc.strftime(format))
        # Convert to Asia/Kolkata time zone
        now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
        #x = datetime.strptime(str(now_asia), "%Y-%m-%dT%H:%M:%S+05:30")
        #x = pytz.timezone('Asia/Calcutta')
        return (now_asia)

        #print(now_asia.strftime(format))
        #print(now_asia.date())

    @staticmethod
    def get_currency_words(currency):
        x=num2words(float(currency), lang="en_IN", to='currency')
        x=x.replace("euro","rupees")
        x=x.replace("cents","paise")
        x=x.title()
        return x

    @staticmethod
    def format_address(x):
        j,k,=0,0
        for i in range(len(x)):
            #print(x[i])
            k+=1
            if x[i] == ',':
              #  print(', '+x[i])
                if j == 1 or k>=25:
                    j = 0
                    #print(x[:i])
                    x = x[:i+1] + '<br>' + x[i+1:]
                    k=0
                else:
                    j += 1
        return x
#Utils.current_time()