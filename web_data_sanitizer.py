# -*- coding: utf-8 -*-

import csv
import os
from datetime import datetime
import re


class WebDataSanitizer(object):

    def __init__(self, filename):
        self.file_name = filename
        self.file_handle = None

    def _check_file_exists(self):
        if os.path.isfile(os.path.abspath(self.file_name)):
            return True
        else:
            # bail out of the program
            raise FileNotFoundError('>> Error: file "{}" not found!'.format(
                self.file_name))

    def _obtain_csv_reader_object(self):
        """ Reads and returns a reader object which will iterate over lines in
        the given csv file and maps the column names.

        Manually close the file handle
        """
        self._check_file_exists()
        self.file_handle = open(self.file_name)
        reader = csv.DictReader(self.file_handle)
        self._check_number_of_columns_in_csv_file(reader)
        try:
            # check if the file contains data
            reader.__next__()

            # reset the file: csv reader obj will not refresh even if the file
            # handle is "seeked" to 0, so re-create reader obj
            self.file_handle.seek(0)
            reader = csv.DictReader(self.file_handle)
        except StopIteration:
            raise ValueError('>> Error: file "{}" does not contain any data!'
                             ''.format(self.file_name))
        else:
            return reader

    def _check_number_of_columns_in_csv_file(self, csv_reader_obj):
        """ If the data file has less columns than the expected number, then
        we have an incomplete data file. Likewise, if we have more columns than
        the expected amount, we have superfluous data that we can't cater for.

        Therefore bail out of the program in each case.
        """
        expected_columns = 7
        if csv_reader_obj.fieldnames is not None:
            if len(csv_reader_obj.fieldnames) == expected_columns:
                return
            else:
                raise ValueError('>> Error: expected {} columns, but found {}!'
                                 ''.format(expected_columns,
                                           len(csv_reader_obj.fieldnames)))
        else:
            raise ValueError(
                '>> Error: no column headings found in source file!')

    def _get_datetime_as_string(self):
        dt = datetime.now()
        return dt.strftime("%Y%m%d_%H%M%S")

    def _get_filename_for_normalized_cleansed_data(self):
        output_dir = './normalized_cleansed_data'
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(
            output_dir, self._get_datetime_as_string()+'_normalized'+'.csv')

    def _get_filename_for_missing_invalid_data(self):
        output_dir = './missing_invalid_data'
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(
            output_dir, self._get_datetime_as_string()+'_invalid'+'.csv')

    def _prepare_output_file_headers(self, filename):
        with open(filename, 'a', encoding='utf-8') as fh:
            field_names = ['date_time', 'domain', 'city', 'country',
                           'browser_version', 'os_version', 'device']
            writer = csv.writer(fh, delimiter=",", quotechar='"')
            writer.writerow(field_names)

    def _write_data_row_to_csv_file(self, filename, data_row):
        with open(filename, 'a', encoding='utf-8') as fh:
            writer = csv.writer(fh, delimiter=",", quotechar='"')
            writer.writerow(
                [data_row['ts'],
                 data_row['domain'],
                 data_row['city'],
                 data_row['country'],
                 data_row['browser_version'],
                 data_row['os_version'],
                 data_row['device']
                ]
            )

    def process_web_data(self):
        reader = self._obtain_csv_reader_object()
        cleansed_data_file = self._get_filename_for_normalized_cleansed_data()
        invalid_data_file = self._get_filename_for_missing_invalid_data()
        self._prepare_output_file_headers(cleansed_data_file)
        self._prepare_output_file_headers(invalid_data_file)

        for row in reader:
            try:
                # check date matches format: yyyy-mm-dd hh:mm:ss
                if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$', row['ts']) \
                        and row['domain'] \
                        and row['city'] \
                        and re.match(r'^\w{2}$', row['country']) \
                        and row['browser_version'] \
                        and row['os_version'] \
                        and row['device']:
                    self._write_data_row_to_csv_file(cleansed_data_file, row)
                else:
                    self._write_data_row_to_csv_file(invalid_data_file, row)
            except KeyError as err:
                raise ValueError('>> Error: could not find expected column '
                                 'heading, please check source file', err.args)
        self.file_handle.close()
        return (os.path.abspath(cleansed_data_file),
                os.path.abspath(invalid_data_file))
