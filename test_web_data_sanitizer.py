#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

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

    def test_process_web_data(self):
        pass
