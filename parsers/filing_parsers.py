
from lxml import etree

def quick_parse(filename):
    parser = etree.XMLParser(recover=True, huge_tree=True)
    tree = etree.parse(filename, parser)
    notags = etree.tostring(tree, encoding='utf8', method='text')

    return notags