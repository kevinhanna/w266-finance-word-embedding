import csv
import os
from google.cloud import storage
from collections import OrderedDict

def get_storage_client():
    dirname = os.path.dirname(__file__)
    client = storage.Client.from_service_account_json(
        dirname + "/../keys/w266-creds.json"
    )
    return client


class Codes:

    @staticmethod
    def get_cik_codes():
        dirname = os.path.dirname(__file__)
        cik_codes = []
        with open(dirname + '/../data/cik_ticker.csv', newline='') as csvfile:
            cik_reader = csv.reader(csvfile, delimiter='|', )
            next(cik_reader, None)  # skip the headers
            for row in cik_reader:
                cik_codes.append(row[0])

        return cik_codes


class Sec_10K:
    user_project = 'w266-kevinhanna' # This needs to be a projec
    storage_bucket = "sec_raw_data"
    dest_dir = "kevin_sandbox/"
    source_dir = "sec_edgar_filings/"
    tmp_dir = "/tmp"

    def __init__(self):
        self.storage_client = get_storage_client()
        self.cik_codes = Codes.get_cik_codes()

    def get_available_10k_filings(self, cik):
        """
        Returns the years for which there are filings for this CIK

        :param cik: CIK for the company you wish to get 10-K's for
        :return: OrderedDict key=year value=filename ordered by year
        """

        bucket = self.storage_client.bucket(self.storage_bucket, self.user_project)
        blobs = bucket.list_blobs(prefix=self.source_dir + str(cik) + "/10-K/")

        return self.__format_sort_filings(blobs)


    def get_filing(self, filepath, tmp_dir=None):
        """
        :param filepath: full path to file
        :param tmp_dir: A temporary directory to store temporary (need to manually delete them when done)
        :return: Filename to downloaded filing
        """

        if tmp_dir is None:
            tmp_dir = self.tmp_dir

        bucket = self.storage_client.bucket(self.storage_bucket, self.user_project)
        blob = storage.Blob(filepath, bucket)

        tmp_filename = tmp_dir + "/" + filepath
        print(tmp_filename)

        os.makedirs(os.path.dirname(tmp_filename), exist_ok=True)

        with open(tmp_filename, "wb") as file_obj:
            self.storage_client.download_blob_to_file(blob, file_obj)

        return tmp_filename




    def __format_sort_filings(self, blobs):
        """
        Returns and OrderedDict of filings passed in as blobs
        :param blobs: likely the result of bucket.list_blobs
        :return: OrderedDict key=year value=filename ordered by year
        """
        results = {}
        for blob in blobs:
            filename = blob.name
            short_year = int(filename.split('-')[-2:-1][0])
            if short_year < 20:
                year = 2000 + short_year
            else:
                year = 1900 + short_year

            results[year] = filename

        return OrderedDict(sorted(results.items()))
