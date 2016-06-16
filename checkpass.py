def checkpas(data):
    for s in set(data):
        if s.isdigit():
            a = True
        if s.isupper():
            b = True
        if s.islower():
            c = True
    if len(data) >= 10 and all([a, b, c]):
        return True
    else:
        return False
