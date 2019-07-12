import sys

from model import documents
from parsers import filing_parsers

def main(*args):
    ciks = documents.Codes.get_cik_codes()
    ten_k = documents.Sec_10K()
    filings = ten_k.get_available_10k_filings(ciks[0])

    # for year, filename in filings.items():
    #     print("year: {}  filename: {}".format(year, filename))
    #     print("tmp_file: {}".format(ten_k.get_filing(filename)))

    file_string = filing_parsers.quick_parse(ten_k.get_filing(filings[2018]))

    foo_file = "/tmp/foo.txt"

    with open(foo_file, "wb") as file_obj:
        file_obj.write(file_string)



if __name__ == '__main__':
    main(*sys.argv)