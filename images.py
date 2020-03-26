import csv
import datetime
import re
import sys
import time

from pathdbapi import *


def usage():
    print('Usage: ' + sys.argv[0] + ' [username] [password] [collection name | "all"]')
    exit(1)


if len(sys.argv) == 4:
    username = sys.argv[1]
    password = sys.argv[2]
    collection = sys.argv[3]
else:
    usage()

host = "http://quip-pathdb"
api = MyApi(host, username, password)

hasNext = True
count = 0
collection_id = 0
collection_name = ''
out_dir = '/data/reports/'
everything = False
stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')

if 'all' in collection.lower():
    everything = True
    images_url = '/listofimages?_format=json'
    lookup_table = api.get_collection_lookup_table()
    name = 'all'
else:
    everything = False
    collection_id, collection_name = api.get_collection_info(collection)
    if len(collection_name) == 0:
        print("Could not find collection:", collection)
        exit(1)
    images_url = '/listofimages/' + str(collection_id) + '?_format=json'
    name = re.sub('\W+', '', collection_name).lower()

with open(out_dir + 'images_' + name + '_' + stamp + '.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Collection', 'Study ID', 'Subject ID', 'Image ID', 'Date'])
    first_nid = 0
    while hasNext:
        count += 1

        url = images_url
        if count > 1:
            url += '&page=' + str(count)

        response = api.get_data(url)
        if len(response) > 0:
            if count == 1:
                first_nid = response[0]['nid'][0]['value']
            if count > 1:
                nid = response[0]['nid'][0]['value']
                if nid == first_nid:
                    break
            for r in response:
                datetime_str = r['created'][0]['value'].replace("T", " ")
                datetime_str = datetime_str.replace("+00:00", "")

                if everything:
                    collection_id = r['field_collection'][0]['target_id']
                    collection_name = lookup_table[collection_id]

                csv_writer.writerow([collection_name, r['studyid'][0]['value'], r['clinicaltrialsubjectid'][0]['value'],
                                     r['imageid'][0]['value'], datetime_str])
        else:
            hasNext = False

exit(0)
