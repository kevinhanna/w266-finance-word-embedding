
from lxml import etree
import re
from copy import deepcopy


def quick_parse(filepath):
    parser = etree.XMLParser(recover=True, huge_tree=True)
    tree = etree.parse(filepath, parser)
    notags = etree.tostring(tree, encoding='utf8', method='text')

    return notags



def parse_10k(filepath):
    """
    Parses the 10-K passed. Returns a dictionary:
        body: The body of the 10-K
    :param filepath:
    :return:
    """
    from bs4 import BeautifulSoup

    results = {}
    with open(filepath) as fp:
        soup = BeautifulSoup(fp, "lxml")

    # Get the header info
    results['headers'] = __parse_sec_header(soup)
    results['documents'] = __parse_documents(soup)

    return results


def __parse_documents(soup):
    # Get all the douments

    result_documents = []
    document_types = []
    documents = soup.find_all('document')

    for doc in documents:

        type_node = doc.find('type')
        type_text = type_node.contents[0].strip()
        seq_node = doc.find('sequence')
        seq_text = seq_node.contents[0].strip()
        desc_node = type_node.find('description')

        if desc_node:
            desc_text = desc_node.contents[0]
        else:
            desc_text = ''

        if type_text.startswith("10-K"):
            is_10_k = True
        else:
            is_10_k = False

        if type_text not in ["XML", "GRAPHIC", "EXCEL", "ZIP"]:
            print(type_text)
            result_documents.append(
                {'is_10_k': is_10_k,
                 'type': type_text,
                 'sequence': seq_text,
                 'description': desc_text,
                 'document': __extract_document_text(doc)}
            )

    return result_documents


def __parse_sec_header(soup):
    sec_header = soup.find("sec-header")

    result = {}

    result['accession_number'] = __get_line_item(sec_header, 'ACCESSION NUMBER:')
    result['conformed_period_of_report'] = __get_line_item(sec_header, 'CONFORMED PERIOD OF REPORT:')
    result['filed_as_of_date'] = __get_line_item(sec_header, 'FILED AS OF DATE:')
    result['company_confirmed_name'] = __get_line_item(sec_header, 'COMPANY CONFORMED NAME:')
    result['central_index_key'] = __get_line_item(sec_header, 'CENTRAL INDEX KEY:')
    result['standard_industrial_classification'] = __get_line_item(sec_header, 'STANDARD INDUSTRIAL CLASSIFICATION:')
    result['state_of_incorporation'] = __get_line_item(sec_header, 'STATE OF INCORPORATION:')
    result['finscal_year_end'] = __get_line_item(sec_header, 'FISCAL YEAR END:')

    return result


def __get_line_item(sec_header, attr_name):
    find_results = re.findall(attr_name + '(.*?)\n', str(sec_header))

    if find_results:
        return find_results[0].strip()
    else:
        return None

def __extract_document_text(document):

    tables = document.find_all('table')
    for table in tables:
        table.decompose()

    return document.get_text()

# def test_parse(filepath):
#     from bs4 import BeautifulSoup
#
#     with open(filepath) as fp:
#         soup = BeautifulSoup(fp, "lxml")
#
#     documents = soup.find_all('document')
#     ten_k = None
#     for doc in documents:
#         type_node = doc.find('type')
#         type_text = type_node.contents[0]
#         desc_node = type_node.find('description')
#         if desc_node:
#             desc_text = desc_node.contents[0]
#         else:
#             desc_text = ''
#
#         if type_text.startswith("10-K"):
#             ten_k = doc
#
#         # print("Type: '{}'  Description: '{}'".format(type_text, desc_text))
#
#     sec_header = soup.find("sec-header")
#     print(sec_header.get_text())
#
#     print(type(sec_header.get_text()))
#
#     print(__parse_sec_header(sec_header))
#
#     tables = soup.find_all('table')
#     for table in tables:
#         table.decompose()
#
#
#     if ten_k is None:
#         print("Failed to find 10-K in {}".format(filepath))
#         return None
#     else:
#         return ten_k.get_text()
#
#
#
#
#
# def test_parse_old(filename):
#     parser = etree.XMLParser(recover=True, huge_tree=True)
#     tree = etree.parse(filename, parser)
#     root = tree.getroot()
#
#     # root = etree.Element("root")
#     # root.append(deepcopy(tree))
#
#     # for foo in root.iter('DOCUMENT'):
#     #     print(foo)
#
#
#     print(root.tag)
#     documents = tree.findall('.//DOCUMENT')
#     # documents = etree.Element("DOCUMENT")
#     print(len(documents))
#
#     for doc in documents:
#         type = doc.xpath('TYPE')
#         seq = doc.xpath('//SEQUENCE')
#
#         if seq is None or len(seq) == 0:
#             seq_text = 'None'
#         else:
#             seq_text = seq[0].text
#
#         print("Type: {}  Seq: {} ".format(type[0].text, seq_text))
#     # for child in tree.iterchildren():
#     #     print(child.tag)
#
#     notags = etree.tostring(tree, encoding='utf8', method='text')
#
#     return notags