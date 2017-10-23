# Coding task to produce a cleansed version of user data

The data sanitizer class is designed to read user data of web-impressions and produce the following output ...

* a cleansed & sanitized version of the source data
* an output file showing invalid or records with missing data



## Execute the script

Designed to run with Python 3 using standard libraries.
```
eg.
$ python3 main.py ./impressions.tsv

>> The sanitized and normalized version of the impressions data can be found:
** ~/Workspace/web_data_sanitiztion_exercise/normalized_cleansed_data/20171023_021922_normalized.csv **

>> The missing/invalid data from the impressions source file can be found:
** ~/Workspace/web_data_sanitiztion_exercise/missing_invalid_data/20171023_021922_invalid.csv **
```
Usage:
```
$ python3 main.py -h                                  
usage: main.py [-h] csv_source_file

This program produces a sanitized version of web user impressions data from a
given csv source file. Along with a file that contains erroneous/invalid data

positional arguments:
  csv_source_file  path to web impressions data (csv).

optional arguments:
  -h, --help       show this help message and exit
```

## Tests

Unit-tests can be run as:
```
$ python3 ./test_web_data_sanitizer.py
```
or
```
$ python3 -m unittest test_web_data_sanitizer.TestWebDataSanitizer
```
