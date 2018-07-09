def flagger(thingum, FLAG):
    for word in FLAG:
        if word in thingum:
            return False
    return True

def dehypdeslash(thing):
    x = thing.split('-')
    x = ' '.join(x)
    x = x.split('/')
    x = ' '.join(x)
    return x

def grabCheck(thing):
    if 'grab' in thing:
        return True
    return False