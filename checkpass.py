def checkpas(data):
    l = len(data)
    a = bool(False)
    b = bool(False)
    c = bool(False)
    for s in set(data):
        if s.isdigit():
            a = True
        if s.isupper():
            b = True
        if s.islower():
            c = True
    if l >= 10 and a and b and c:
        return True
    else:
        return False
