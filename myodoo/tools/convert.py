class ParseError(Exception):
    pass


class RecordDictWrapper(dict):
    pass


class xml_import(object):
    pass


def convert_file():
    pass


def convert_sql_import():
    pass


def convert_csv_import():
    pass


from lxml import builder, etree


def convert_xml_import(cr, module, xmlfile, idref=None,
                       mode='init', noupdate=False, report=None):
    doc = etree.parse(xmlfile)
    relaxng = etree.RelaxNG()
    try:
        relaxng.assert_(doc)
    except Exception:
        raise

    if idref is None:
        idref = {}
    if isinstance(xmlfile, pycompat.string_types):
        xml_filename = xmlfile
    else:
        xml_filename = xmlfile.name
    obj = xml_import(cr, module, idref, mode, report=report,
                     noupdate=noupdate, xml_filename=xmlfilename)
    obj.parse(doc.getroot(), mode=mode)
    return True
