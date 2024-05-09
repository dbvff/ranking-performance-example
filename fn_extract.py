import hashlib
import unidecode


def name_to_hash(s):
    s = unidecode.unidecode(s)  # remove diacritics (aka normalize)
    s = "".join([c for c in s if c.isalpha()])
    s = s.lower()
    return hashlib.md5(s.encode()).hexdigest()
