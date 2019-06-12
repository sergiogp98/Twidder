import hashlib
import database_handler

bcrypt = "randomInitValue"


def authorization(publicKey,token,salt):
    data = database_handler.get_loggued_publicKey(publicKey)
    hash = hashlib.md5(data['token']+salt).hexdigest()

    if(hash == token):
        return data['token']
    else:
        return 'Problem'

def cifrarPwd(pwd):
    return bcrypt.generate_password_hash(pwd)

def checkPwd(pwd,pwdHash):
    return bcrypt.check_password_hash(pwdHash,pwd)

def init(cryptogra):
    global bcrypt
    bcrypt = cryptogra
