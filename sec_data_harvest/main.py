import csv
import sys
from sec_edgar_downloader import Downloader


def get_cik_codes():
    cik_codes = []
    with open('./data/cik_ticker.csv', newline='') as csvfile:
        cik_reader = csv.reader(csvfile, delimiter='|', )
        next(cik_reader, None)  # skip the headers
        for row in cik_reader:
            cik_codes.append(row[0])

    return cik_codes


def fetch_statements(cik, downloader):
    print("Fetching CIK: {}".format(cik))
    downloader.get_all_available_filings(cik, 1)


def main(*args):
    edgar_dl = Downloader("/home/khanna/Transfer/financial_reports")

    all_cik_codes = get_cik_codes()

    for i in range(len(all_cik_codes)):
        cik = all_cik_codes[i]
        print("Fetching CIK: {}  {} of {}".format(cik, i, len(all_cik_codes)))
        fetch_statements(cik, edgar_dl)


if __name__ == '__main__':
    main(*sys.argv)
