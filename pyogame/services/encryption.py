from cryptography.fernet import Fernet
import hashlib
import pyogame.settings
import datetime


SECRET_KEY = pyogame.settings.SECRET_KEY.encode()
cipher = Fernet(SECRET_KEY)


def encrypt(text):
    return cipher.encrypt(text.encode()).decode()


def decrypt(text):
    return cipher.decrypt(text.encode()).decode()


def hash_pin(request):
    return str(''.join(filter(str.isdigit, hashlib.sha3_512(request.user.email.encode()).hexdigest()))[0:8])


def hash(user):
    return hashlib.sha3_512(
        '@'.join([user.email, user.username, user.password, str(user.date_joined), SECRET_KEY]).encode()
    ).hexdigest()
