import chardet


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
    # print u"%s --[%s]-> %s" % (text, out, text.decode(out))
    return text.decode(out)
