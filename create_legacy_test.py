with open('h:/VSCode/docx-preview-cicool/test_legacy.doc', 'wb') as f:
    # CFBF Magic Header (Word 97-2003 binary file)
    f.write(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1' + b'\x00' * 504)
print('Legacy .doc dummy created.')
