try:
    fh = open('test.file', 'w')
    fh.write('line')
except IOError:
    print('error')
finally:
    print('ok')
    fh.close()

