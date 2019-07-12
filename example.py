import sys

from model import documents
from parsers import filing_parsers

def main(*args):
    ciks = documents.Codes.get_cik_codes()
    ten_k = documents.Sec_10K()

    # Get a list of 10-K's (just grabbing the first CIK)
    yearly_filing_files = ten_k.get_available_10k_filings('1001039')

    # Can iterate though filings
    # for year, filename in filings.items():
    #     print("year: {}  filename: {}".format(year, filename))
    #     print("tmp_file: {}".format(ten_k.get_filing(filename)))

    # Parse the file (currently just strips XML tags
    file_string = filing_parsers.test_parse(ten_k.get_filing(yearly_filing_files[2018]))

    # Put the file somewhere, this will be BigQuery or Cloud Storage
    foo_file = "/tmp/foo.txt"
    with open(foo_file, "w") as file_obj:
        file_obj.write(file_string)



if __name__ == '__main__':
    main(*sys.argv)