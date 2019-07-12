
from lxml import etree
from copy import deepcopy


def quick_parse(filepath):
    parser = etree.XMLParser(recover=True, huge_tree=True)
    tree = etree.parse(filepath, parser)
    notags = etree.tostring(tree, encoding='utf8', method='text')

    return notags

def test_parse(filepath):
    from bs4 import BeautifulSoup

    with open(filepath) as fp:
        soup = BeautifulSoup(fp, "lxml")

    documents = soup.find_all('document')
    ten_k = None
    for doc in documents:
        type_node = doc.find('type')
        type_text = type_node.contents[0]
        desc_node = type_node.find('description')
        if desc_node:
            desc_text = desc_node.contents[0]
        else:
            desc_text = ''

        if type_text.startswith("10-K"):
            ten_k = doc

        print("Type: '{}'  Description: '{}'".format(type_text, desc_text))

    tables = soup.find_all('table')
    for table in tables:
        table.decompose()


    if ten_k is None:
        print("Failed to find 10-K in {}".format(filepath))
        return None
    else:
        return ten_k.get_text()





def test_parse_old(filename):
    parser = etree.XMLParser(recover=True, huge_tree=True)
    tree = etree.parse(filename, parser)
    root = tree.getroot()

    # root = etree.Element("root")
    # root.append(deepcopy(tree))

    # for foo in root.iter('DOCUMENT'):
    #     print(foo)


    print(root.tag)
    documents = tree.findall('.//DOCUMENT')
    # documents = etree.Element("DOCUMENT")
    print(len(documents))

    for doc in documents:
        type = doc.xpath('TYPE')
        seq = doc.xpath('//SEQUENCE')

        if seq is None or len(seq) == 0:
            seq_text = 'None'
        else:
            seq_text = seq[0].text

        print("Type: {}  Seq: {} ".format(type[0].text, seq_text))
    # for child in tree.iterchildren():
    #     print(child.tag)

    notags = etree.tostring(tree, encoding='utf8', method='text')

    return notags