import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def validateEmail(email):

    if (re.search(regex, email)):
        pass
    else:
        print("Invalid email")
        exit()