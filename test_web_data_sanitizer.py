#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import csv
import os

from web_data_sanitizer import WebDataSanitizer


class TestWebDataSanitizer(unittest.TestCase):

    def test_file_exists(self):
        wds = WebDataSanitizer('./test_data/test_data_1.csv')
        self.assertTrue(wds._check_file_exists())

    def test_file_not_found(self):
        wds = WebDataSanitizer('./test_data/test_data_XX.csv')
        with self.assertRaises(FileNotFoundError):
            wds._check_file_exists()

    def test_csv_reader_object_has_data(self):
        wds = WebDataSanitizer('./test_data/test_data_1.csv')
        reader = wds._obtain_csv_reader_object()
        rows = sum(1 for row in reader)
        self.assertEqual(rows, 8)
        wds.file_handle.close()

    def test_csv_reader_object_with_no_data_rows(self):
        wds = WebDataSanitizer('./test_data/test_data_2.csv')
        try:
            with self.assertRaises(ValueError):
                wds._obtain_csv_reader_object()
        finally:
            wds.file_handle.close()

    def test_csv_reader_with_empty_source_file(self):
        wds = WebDataSanitizer('./test_data/test_data_3.csv')
        try:
            with self.assertRaises(ValueError):
                wds._obtain_csv_reader_object()
        finally:
            wds.file_handle.close()

    def test_unexpected_number_of_columns_in_csv_file(self):
        wds = WebDataSanitizer('./test_data/test_data_4.csv')
        try:
            with self.assertRaises(ValueError):
                wds._obtain_csv_reader_object()
        finally:
            wds.file_handle.close()

    def test_unexpected_column_heading_name_in_csv_file(self):
        wds = WebDataSanitizer('./test_data/test_data_4.csv')
        try:
            with self.assertRaises(ValueError):
                wds.process_web_data()
        finally:
            wds.file_handle.close()

    def test_process_web_data(self):
        cleansed_data = None
        missing_data = None
        try:
            # test file contains 4 valid and 4 invalid rows of data
            wds = WebDataSanitizer('./test_data/test_data_1.csv')
            cleansed_data, missing_data = wds.process_web_data()

            with open(cleansed_data, 'r') as fh1:
                reader = csv.reader(fh1)
                # count rows including header
                row_count_clean = sum(1 for row in reader)
            self.assertEqual(row_count_clean, 5)

            with open(missing_data, 'r') as fh2:
                reader = csv.reader(fh2)
                # count rows including header
                row_count_invalid = sum(1 for row in reader)
            self.assertEqual(row_count_invalid, 5)
        finally:
            if os.path.isfile(cleansed_data):
                os.remove(cleansed_data)
            if os.path.isfile(missing_data):
                os.remove(missing_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
