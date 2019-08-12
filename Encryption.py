random_number = int('3141592653589793238462643383279502' +
                    '8841971693993751058209749445923078' +
                    '16406286208998628034825342117067')


def asciidata(data):
    datanew = ""
    for i in data:
        val = ord(i)
        if (val > 126 or val < 9) and not val == 5:
            print("Character passed -->", val)
        else:
            datanew += i

    return datanew


def encrypt_decrypt(text, code, action, skip=0):
    if action.lower() == "d":
        action = -1
    elif action.lower() == "e":
        action = 1

    code *= random_number
    # code is a number
    code = [int(i) for i in list(str(code))]

    new = ""
    l = len(code)
    for i in range(len(text)):
        letter = text[i]
        if ord(letter) >= 32:
            letter = ord(letter) + action*code[(i+skip) % l]
            # ASCII code after 127 is basically not defined for general
            # uses.
            if letter < 32:
                difference = 31-letter
                letter = 126-difference

            if letter > 126:
                difference = letter - 126
                letter = 31+difference

            letter = chr(letter)

        if letter == "\n" and action > 0:
            letter = chr(5)
        if ord(letter) == 5 and action < 0:
            letter = "\n"

        # print([text[i]],"---->",[letter], "by", action*code[i%l])
        new += letter
    return new


def encrypt(text, code, skip=0):
    return encrypt_decrypt(text, code, 'e', skip)


def decrypt(text, code):
    return encrypt_decrypt(text, code, 'd')


def formted_methods(raw, code, action):
    action = action.lower()
    if action not in ('d', 'e'):
        raise Exception
    raw = raw.lstrip()
    if raw[:6] == "00es00":
        encrypted = True
    else:
        if action == 'd':
            return 0
        else:
            encrypted = False

    if encrypted:
        e = raw.index("00ed00")
        end = int(raw[raw.index("00es00")+6:e])
        n_char = end
        start = raw.index("?0x0x0x527") + 10
        end = end+start
        after = raw[end+1:]
        content = raw[start: end]
        if action == "d":
            new = decrypt(content, code)
            new += after
            return new
        else:
            new = content
            new += encrypt(after, code, skip=n_char)
            new = add_pretext(new)
            return new
    else:
        new = add_pretext(encrypt(raw, code))
        return new


def add_pretext(text):
    s = "00es00" + str(len(text)) + "00ed00"
    ini = "?0x0x0x527"
    return s+"\n"+ini+text


class WeakCodeError(Exception):
    pass


def make_code(code):
    try:
        code = int(code)

        if len(str(code)) > 20 or len(str(code)) < 4:
            raise WeakCodeError

        if code % 100 == 0:
            raise WeakCodeError

        return code

    except ValueError:
        raise ValueError
