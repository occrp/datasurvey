import chardet
from hashlib import sha1


def guess_encoding(text):
    if text is None or len(text) == 0:
        return
    if isinstance(text, unicode):
        return text
    enc = chardet.detect(text)
    out = enc.get('encoding', 'utf-8')
    if out is None:
        # Awkward!
        return text
    return text.decode(out)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)


def checksum(filename):
    """Generate a hash for a given file name."""
    hash = sha1()
    with open(filename, 'rb') as fh:
        while True:
            block = fh.read(2 ** 10)
            if not block:
                break
            hash.update(block)
    return hash.hexdigest()
