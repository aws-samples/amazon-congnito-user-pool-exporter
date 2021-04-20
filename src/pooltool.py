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

import boto3
from botocore.exceptions import ClientError
import argparse
import os
from datetime import datetime
import yaml
import json
import sys
import ast
from common import utilities

def import_file(args):
    print("Not implemented")


def export_file(args):
    export_file = args.file
    export_format = args.format
    settings_file = args.settings_file
    verbose = args.verbose
    profile_override = args.profile
    region_override = args.region
    pool_id = args.id

    settings = utilities.read_settings_file(args.settings_file)

    if profile_override is not None:
        settings['profile'] = profile_override
    if region_override is not None:
        settings['region'] = region_override

    # print("Exporting file")
    # print("File: "+export_file+"\nFormat: "+export_format+"\nSettings file: "+settings_file+"\nVerbose: "+str(verbose)+"\nProfile override: "+str(profile_override)+"\nRegion override:"+str(region_override))
    # print("Settings File")
    # print(settings)

    pool_data = get_pool_data(settings, pool_id, args.verbose)

    #print(json.dumps(pool_data, indent=4, default=utilities.datetime_converter))
    utilities.write_to_file(export_file, format, pool_data)


def get_pool_data(settings, pool_id, verbose=False):
    session = boto3.session.Session(profile_name=settings['profile'])
    client = session.client('cognito-idp', region_name=settings['region'])
    users = []

    response = client.get_csv_header(
        UserPoolId=pool_id
    )
    csv_headers = response['CSVHeader']

    if verbose:
        print(json.dumps(csv_headers, indent=4))

    response = utilities.list_users_helper(client, pool_id, None)
    users = users + response['Users']

    while 'PaginationToken' in response:
        pagination_token = response['PaginationToken']
        response = utilities.list_users_helper(client, pool_id, pagination_token)
        users = users + response['Users']

    if verbose:
        print(json.dumps(users, indent=4, default=utilities.datetime_converter))

    return {
        "Users": users,
        "CSVHeaders": csv_headers
    }


def main():
    parser = argparse.ArgumentParser()
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--settings_file', help="settings file, if not specified, assumes a 'settings.txt' is locate in the same path as this script", default='settings.txt')

    subparsers = parser.add_subparsers(dest='command')

    export_parser = subparsers.add_parser('export', help="exports user pool to file", parents=[common_parser])

    export_subparsers = export_parser.add_subparsers(dest='action')

    parser_export_user_pool = export_subparsers.add_parser('userpool', help="Exports user pool")
    parser_export_user_pool.add_argument('--file', help="[Required] output file path", required=True)
    parser_export_user_pool.add_argument('--id', help="[Required] userpool id", required=True)
    parser_export_user_pool.add_argument('--verbose', help="display json output of user pool", required=False, default=False, action='store_true')
    parser_export_user_pool.add_argument('--format', help="output file type [json or csv]; defaults to csv", required=False, default='csv')
    parser_export_user_pool.add_argument('--region', help="region name; overrides value from settings.txt", required=False, default=None)
    parser_export_user_pool.add_argument('--profile', help="aws profile name; overrides value from settings.txt", required=False, default=None)


    args = parser.parse_args()

    if args.command == 'export':
        if 'file' in args:
          export_file(args)
        else:
          parser_export_user_pool.print_help()



if __name__ == "__main__":main()
