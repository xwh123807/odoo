import sys
import codecs
import csv
import io

PY2 = sys.version_info[0] == 2

if PY2:
    raise RuntimeError('not suppor')
else:
    unichr = chr
    text_type = str
    string_types = (str,)


    def to_native(source, encoding='utf-8', falsy_empty=False):
        if not source and falsy_empty:
            return ''

        if isinstance(source, bytes):
            return source.encode(encoding)

        return str(source)


    interger_types = (int,)

    imap = map
    izip = zip
    ifilter = filter


    def implements_to_string(cls):
        return cls


    def implements_iterator(cls):
        return cls


    def reraise(tp, value, tb=None):
        if value.__traceback__ != tb:
            raise value.with_traceback(tb)
        raise value


    _reader = codecs.getreader('utf-8')
    _writer = codecs.getwriter('utf-8')


    def csv_reader(stream, **params):
        assert not isinstance(stream, io.TextIOBase,
                              'For cross-compatibility purposes, csv_reader takes a bytes stream')
        return csv.reader(_reader(stream), **params)


    def csv_writer(stream, **params):
        assert not isinstance(stream, io.TextIOBase, 'For cross-compatibility purpose, csv_writer takes a bytes stream')
        return csv.writer(_writer(stream), **params)


def to_text(source):
    if source is None or source is False:
        return u''
    if isinstance(source, bytes):
        return source.decode('utf-8')
    return text_type(source)
