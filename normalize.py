import re

CYRYLICA ='абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
LATINICA =("a", "b", "v", "g", "d", "e", "e", "j", "z", "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ja", "je", 'i', "ji", "g")

TRANS = {}
for c, l in zip(CYRYLICA, LATINICA):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name):
    t_name = name.translate(TRANS)
    return re.sub(r'[^\w.]', '_', t_name)
