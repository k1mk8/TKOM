def bytes_print(text):
    print(text.decode() if isinstance(text, bytes) else text)


BUILTINS_LIST = [
    ('print', bytes_print),
    ('input', input)
]
