""" Signup and Рassword reset module 

Contains class AccountProc that contains following functions:
- initiate_proc: initiates process, 
uses auxiliary functions to generate code, token and send email
- check_proc: checks than token and code are correct
- check_token: checks that gotten token exists
- get_email: returns email by gotten token
- clear_proc: deletes code object
- ban_email: checks that user can initiate the process once every 15 minutes
- ban_code: checks code bruteforce (5 attempts to ban)
- get_step: returns step value for checking sequence of user's actions
- set_step: sets new step value for checking sequence of user's actions
- _generate_code: generate email code
- _generate_token: generate token for cookie and tracking
- _unique_code_token: checks that code and token are unique
- _build_code: creates code object
- _send_email: sends code to email

Included mail functional is just for testing signup_* and reset_password_* 
pages.
You need to set your own EMAIL_BACKEND for your project and use it 
instead of this.

"""


import secrets
from datetime import datetime, timedelta

from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Q

from .models import Code


class AccountProc():

    @staticmethod
    def _unique_code_token(candidate):
        if (Code.objects.filter(Q(code_value=candidate) | 
                                Q(code_token=candidate)).exists()):
            return False
        else:
            return True

    @classmethod
    def _generate_code(cls):
        rnd = secrets.SystemRandom()
        code = str(rnd.randint(10000000, 99999999))
        if cls._unique_code_token(code):
            return code
        else:
            cls._generate_code()

    @classmethod
    def _generate_token(cls):
        token = secrets.token_hex()
        if cls._unique_code_token(token):
            return token
        else:
            cls._generate_token()

    @staticmethod
    def _build_code(code, email, token):
        now = datetime.now()
        Code.create_code(code, email, now, token)

    @classmethod
    def _send_email(cls, code, email):
        text = f'Your code: {code}. If you did not ask a code - tell us!'
        send_mail('Lister', text, 'from@lister.com', 
                    [email], fail_silently=False, )

    @classmethod
    def initiate_proc(cls, email):
        code = AccountProc._generate_code()
        token = AccountProc._generate_token()
        cls._build_code(code, email, token)
        cls._send_email(code, email)
        return token

    @staticmethod
    def check_proc(user_code, token):
        if (Code.objects.filter(code_value=user_code, 
                                code_token=token).exists()):
            return True
        return False

    @staticmethod
    def check_token(token):
        if Code.objects.filter(code_token=token).exists():
            return True
        return False

    @staticmethod
    def get_email(token):
        email = Code.objects.get(code_token=token).code_email
        return email

    @staticmethod
    def clear_proc(email):
        Code.objects.filter(code_email=email).delete()

    @staticmethod
    def ban_email(email):
        if Code.objects.filter(code_email=email).exists():
            created = Code.objects.get(code_email=email).code_created
            if (created + timezone.timedelta(minutes=15) > timezone.now()):
                return True
            else:
                Code.objects.filter(code_email=email).delete()
        return False

    @staticmethod
    def ban_code(token):
        if Code.objects.filter(code_token=token).exists():
            code = Code.objects.get(code_token=token)
            code.code_attempt += 1
            code.save()
            attempt = code.code_attempt
            if (attempt > 4):
                return 1
            else:
                return 0
        else:
            return 2

    @staticmethod
    def get_step(token):
        if Code.objects.filter(code_token=token).exists():
            step = Code.objects.get(code_token=token).code_step
            return step
        else:
            return -1

    @staticmethod
    def set_step(token, step):
        if Code.objects.filter(code_token=token).exists():
            code = Code.objects.get(code_token=token)
            code.code_step = step
            code.save()
