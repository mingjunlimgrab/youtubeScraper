

def dehypdeslash(title):
    result1 = title
    if '-' in result1:
        result1 = title.split('-')
        result1 = ' '.join(result1)
    if '/' in result1:
        result1 = result1.split('/')
        result1 = ' '.join(result1)
    return result1


def flagger(title, flag):
    for word in flag:
        if word in title:
            return False
    return True

def grabCheck(title):
    if 'grab' in title:
        return True
    return False


