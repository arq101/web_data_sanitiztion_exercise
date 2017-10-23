#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from web_data_sanitizer import WebDataSanitizer


def arg_parser():
    parser = argparse.ArgumentParser(
        description='This program produces a sanitized version of web user '
                    'impressions data from a given csv source file. Along with '
                    'a file that contains erroneous/invalid data')
    parser.add_argument('csv_source_file', action="store", type=str,
                        help='path to web impressions data (csv).')
    return parser.parse_args()


def main():
    args = arg_parser()

    web_sanitizer = WebDataSanitizer(args.csv_source_file)
    cleansed_data, invalid_data = web_sanitizer.process_web_data()
    print('>> The sanitized and normalized version of the impressions data can '
          'be found:')
    print('** {} **'.format(cleansed_data))
    print()
    print('>> The missing/invalid data from the impressions source file can '
          'be found:')
    print('** {} **'.format(invalid_data))


if __name__ == '__main__':
    main()