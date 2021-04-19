# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from datetime import datetime
import decimal
import json
import boto3
import os
from typing import Dict, Any, List
from botocore.exceptions import ClientError
import logging

def datetime_converter(dto):
    if isinstance(dto, datetime):
        return dto.__str__()

def list_users_helper(client, pool_id, pagination_token):
    if pagination_token is not None:
        return client.list_users(
            UserPoolId = pool_id,
            PaginationToken = pagination_token
        )
    else:
        return client.list_users(
            UserPoolId = pool_id
        )


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def write_to_file(filename, format, pool_data):
    users = pool_data['Users']
    csv_headers = pool_data['CSVHeaders']
    header_string = ','.join(csv_headers)
    outfile = open(filename, 'w')
    outfile.write(header_string+"\n")
    for user in users:
        user_string = None
        attributes = user['Attributes']
        for header in csv_headers:
            value = next((item['Value'] for item in attributes if item["Name"] == header), '')
            if header == 'cognito:username':
                value = user['Username']
            if (header.lower().endswith('enabled') or header.lower().endswith('verified')) and value == '':
                value = 'false'
            if user_string is None:
                user_string = value
            else:
                user_string = user_string+","+value
        outfile.write(user_string+"\n")
    return

def read_setting_line(line):
    return line.split('=')[1].lstrip().rstrip()

def read_settings_file(filename):
    settings = {}

    with open(filename) as settings_file:
        line = settings_file.readline()
        while line:
            if line.upper().startswith('PROFILE'):
                settings['profile'] = read_setting_line(line)

            elif line.upper().startswith('REGION'):
                settings['region'] = read_setting_line(line)

            elif line.upper().startswith('ENDPOINT_TYPE'):
                settings['endpoint_type'] = read_setting_line(line)

            elif line.upper().startswith('ENDPOINT'):
                settings['endpoint'] = read_setting_line(line)

            line = settings_file.readline()

    return settings
