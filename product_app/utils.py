
import string  
import secrets 


def random_string(num):   
    """
    Generates a random string of length 'num' with letters and digits.
    """
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
    return str(res)
