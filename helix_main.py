'''
Copyright 2021 FireEye, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
/***************************************************************************************
*    Title: Helix main script
*    Author: Mahmoud Eraqi
*    Date: 09/05/2021
*    Code version: v1.2
*    Availability: github(to be detailed)
*
*	Description: This code serves are a starter kit utilizing the Helix APIs.
*				 You must be a Helix subscriber to use this script effectively
*
***************************************************************************************/
'''

import argparse
import datetime
import json
import pprint
import requests

from configparser import ConfigParser
from requests.models import InvalidURL


def csv_file_creation(text_data, file_name):
    """
    CSV creation function
    Takes original response data as text_data and creates csv file.

    text_data -- response data from API call 
    file_name -- user specified file name ending with .csv
    """
    text_file = open(file_name, "w")
    text_file.writelines(text_data)
    text_file.close()


def search_helix_alerts(search_data, file_name, query_size, configs, headers):
    """
    Search function call, this funcation takes in multiple arguments
    to make a call to the Helix Search API endpoint.

    search_data -- user input MQL query string
    file_name -- name of file for output data 
    query_size -- amount of data getting back from API call
    configs -- config file data to authenticate the API call
    headers -- header data for API call

    returns Helix Search API endpoint data/response
    """
    pprint.pprint("Requesting helix alerts based on metaclass (beta version)")
    payload_json_csv = {
        "query": search_data,
        "format": "csv",
        "options": {
            "page_size": query_size
            }
        }
    url = "{}/helix/id/{}/api/v1/search".format(configs['base_url'],
                                                configs['helix_id'])
    payload_csv = json.dumps(payload_json_csv)

    try:
        response_csv = requests.post(url, headers=headers, data=payload_csv)

    except InvalidURL:
        pprint.pprint("FATAL ERROR (Invalid URL): Check configurations"
                      " section for any misstyped values or extra spaces,"
                      " then re-run program")
        exit()

    if response_csv.status_code == 200:
        pprint.pprint("creating CSV text....")
        csv_file_creation(response_csv.text, file_name)

    else:
        pprint.pprint(
            "Error with Helix code: {} text: {}".format
            (response_csv.status_code, response_csv.text)
        )
        if response_csv.status_code == 401:
            pprint.pprint(
                "Unable to authenticate with Helix error: {}".format
                (response_csv.text))
        else:
            raise Exception(
                "Error with Helix code: {} text: {}".format
                (response_csv.status_code, response_csv.text))


def main():
    """
    main function, handles all command line arguments, and 
    points them to the proper funcation
    """
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    # setting variables
    helix_info = config_object['HELIXCONFIG']
    t = datetime.datetime.now()

    # alert api url
    headers = {
        'x-fireeye-api-key': helix_info["api_key"],
        'Content-Type': 'application/json'
    }

    parser = argparse.ArgumentParser(description='Handling Helix API.')
    parser.add_argument("-id",
                        help="Not yet available")

    parser.add_argument("-q", "--query_search",
                        nargs='?',
                        default="has:class",
                        type=str,
                        help="Using MQL format syntax,"
                        " search for log data within helix")

    parser.add_argument("-hd", "--helix_date",
                        nargs='+',
                        help="set up a custom date of when to"
                        " pull the dates (still in development)")

    parser.add_argument("-qs", "--query_size",
                        nargs='?',
                        default=20,
                        type=int,
                        help="All APIs have a query size option"
                        " where you can control how much data you"
                        " would like to pull out input any real number"
                        " from 1-1000 (as this is the limit of the query"
                        " size the Helix APIs allow)")

    parser.add_argument("-csv", "--csv_file_name",
                        nargs='?',
                        default="helix_data_output"
                                "["+(t.strftime("%Y-%m-%d %H:%M:%S"))+"].csv",
                        type=str,
                        help="write custom file name i.e. 'file_name_here.csv',"
                        " or default"
                        " 'helix_data_output[date/timestamp of data].csv'"
                        " will be the give name")

    parser.add_argument("-aa", "--add_alert",
                        help="Not yet available")
    args = parser.parse_args()

    if args.query_search:
        mql_search_data = args.query_search
        search_helix_alerts(mql_search_data, args.csv_file_name,
                            args.query_size, helix_info, headers)
        pprint.pprint("CSV created")
        exit()

if __name__ == '__main__':
    main()
