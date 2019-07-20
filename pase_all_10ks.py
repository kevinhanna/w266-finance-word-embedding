import logging
import sys
import os

from model import documents
from parsers import filing_parsers


def main(*args):
    ciks = documents.Codes.get_cik_codes()
    ten_k_filing = documents.Sec10kFilings()
    start_at = '6201'
    do_parse = False

    for cik in ciks:

        if cik == start_at:
            do_parse = True

        if not do_parse:
            continue

        # Get a list of 10-K's
        yearly_filing_files = ten_k_filing.get_available_10k_filings(cik)

        for year, filename in yearly_filing_files.items():
            local_tmp_dir = '/tmp'
            filepath = ten_k_filing.fetch_10k_filing(filename, local_tmp_dir=local_tmp_dir)
            parsed_filing = filing_parsers.parse_10k(filepath, cik, year)

            # Store documents
            new_10k = documents.Sec10k(parsed_filing.get('headers'), parsed_filing.get('documents'))
            new_10k.save()

            # Cleanup tmp file
            os.remove(local_tmp_dir + "/" + filename)

        logging.info("Done parsing cik: {}".format(cik))


    # # Print Headers:
    # headers = parsed_filing.get('headers')
    #
    # for key, value in headers.items():
    #     print("{}: {}".format(key, value))
    #
    # # Write Documents
    # ten_k_documents = parsed_filing.get('documents')
    #
    # for document_obj in ten_k_documents:
    #
    #     type = document_obj.get('type')
    #     sequence = document_obj.get('sequence')
    #     document = document_obj.get('document')
    #
    #     filepath = "/tmp/parsed/" + cik + "/" + str(year) + "/" + type + "_" + sequence + ".txt"
    #     print("File: {}".format(filepath))
    #
    #     os.makedirs(os.path.dirname(filepath), exist_ok=True)
    #
    #     with open(filepath, "w") as file_obj:
    #         file_obj.write(document)

    # # Put the file somewhere, this will be BigQuery or Cloud Storage
    # foo_file = "/tmp/foo.txt"
    # with open(foo_file, "w") as file_obj:
    #     file_obj.write(file_string)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main(*sys.argv)