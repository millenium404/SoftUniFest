

def validate_phone(string):
    string = string.replace(' ', '')
    if string[0] == '0' or string[:4] == '+359':
        string = string.replace('+', '')
        if string.isdigit():
            return True
    return False

def validate_card(string):
    string = string.replace(' ', '')
    if string.isdigit() and len(string) == 16:
        return True
    return False


def validate_exp_date(string):
    if len(string) != 5 or '/' not in string:
        return False
    try:
        string = string.split('/')
        month = int(string[0])
        year = int(string[1])
    except:
        return False
    if month > 12 or year < 21 or year > 30:
        return False
    return True
