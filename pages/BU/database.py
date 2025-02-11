from deta import Deta
DETA_KEY = "b0hisdr72mx_tynwrFs5VwJtxoc5BFKrEV1wDrPEGR3j"

deta = Deta(DETA_KEY)


db = deta.Base("user_db")



def insert_user(username, name, password):
    """Returns the user on a succesful user creation, otherwise raiser and error"""
    return db.put({"key": username, "name": name, "password": password})

insert_user("pparker","Peter Parkert", "abc123")