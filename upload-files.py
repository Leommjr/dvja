#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import sys
from datetime import datetime
import json
import os
import requests


def upload_results(  # set verify to False if ssl cert is self-signed
    host,
    api_key,
    scanner,
    result_file,
    prod_name,
    verify=False,
    ):
    API_URL = 'http://' + host + '/api/v2'
    IMPORT_SCAN_URL = API_URL + '/import-scan/'
    AUTH_TOKEN = 'Token ' + api_key

    headers = dict()
    json = dict()
    files = dict()
    headers['Authorization'] = AUTH_TOKEN

    json['minimum_severity'] = 'Low'
    json['scan_date'] = datetime.now().strftime('%Y-%m-%d')
    json['verified'] = verify
    json['product_name'] = prod_name
    json['active'] = True
    json['scan_type'] = scanner
    json['test_title'] = scanner \
        + ' import from frankfurt-security-testing'
    json['engagement_name'] = 'frankfurt-security-testing'+datetime.now().strftime('%Y-%m-%d')
    json['product_type_name'] = 'Teste'
    json['auto_create_context'] = True

    # Prepare file data to send to API

    files['file'] = open(result_file)

    # Make request to API

    response = requests.post(IMPORT_SCAN_URL, headers=headers,
                             files=files, data=json, verify=verify)
    print(response.content)
    return response.status_code


if __name__ == '__main__':
    parser = \
        argparse.ArgumentParser(description='CI/CD integration for DefectDojo'
                                )
    parser.add_argument('--api_key', help='API Key', required=True)
    parser.add_argument('--result_file', help='Scanner file',
                        required=True)
    parser.add_argument('--scanner', help='Type of scanner',
                        required=True)
    parser.add_argument('--host', help='Defect Dojo Host',
                        required=True)

    parser.add_argument('--name', help='Product Name',
                        required=True)

    args = vars(parser.parse_args())
    host = args['host']
    api_key = args['api_key']
    result_file = args['result_file']
    scanner = args['scanner']
    prod_name = args['name']

    result = upload_results(host, api_key, scanner, result_file, prod_name)

    if result == 201:
        print('Successfully uploaded the results to Defect Dojo')
    else:
        print('Something went wrong, please debug ' + str(result))
