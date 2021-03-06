import csv
import datetime
import re
import sys
import time

from combine_data import *
from mongoapi import *
from pathdbapi import *

usr_details = {}


def get_date(ii, xx):
    created_date = ""
    if "created_date" in ii:
        created_date = ii['created_date']
    else:
        if "submit_date" in xx:
            created_date = xx['submit_date']

    # 2020-03-03T16:25:13.299Z
    return created_date


def get_peep(i, X):
    creator_str = ""
    if "creator" in i:
        creator_num = i['creator']
        if creator_num.isnumeric():
            p = "/user/" + creator_num + "?_format=json"
            if creator_num in usr_details.keys():
                creator_str = usr_details[creator_num]
            else:
                rr = api.get_data(p)
                if len(rr) > 0:
                    usr_details[creator_num] = rr['name'][0]['value']
                    creator_str = rr['name'][0]['value']
    elif "source" in i:
        creator_str = X['source']
    else:
        creator_str = "Computer"

    return creator_str.capitalize()


def featuremap(my_writer, my_img, none_row):
    my_list = api.get_featuremaps(my_img['nid'])
    current_type = "Featuremap"
    if len(my_list) > 0:
        for i in my_list:
            # print(i)
            created = i['created'][0]['value']
            if len(i['execution_id']) > 0:
                execution_id = i['execution_id'][0]['value']
            else:
                # Compensating for database
                execution_id = i['field_map_type'][0]['value']

            if 'executed_by' in i:
                if len(i['executed_by']) > 0:
                    executed_by = i['executed_by'][0]['value']
                else:
                    executed_by = ""
            else:
                executed_by = ""

            my_writer.writerow(
                [collection_name, my_img['studyid'], my_img['subjectid'], my_img['imageid'], current_type, execution_id,
                 executed_by, created])
    else:
        none_row[len(none_row) - 2] = current_type
        my_writer.writerow(none_row)


def heatmap(my_writer, my_img, none_row):
    current_type = "Heatmap"
    my_list = heat(my_img)
    if len(my_list) > 0:
        for i in my_list:
            # print(i)
            # source, execution_id, computation (no date)
            X = i['provenance']['analysis']
            current_type = X['computation'].capitalize()
            # TODO: computation
            my_writer.writerow(
                [collection_name, my_img['studyid'], my_img['subjectid'], my_img['imageid'], current_type,
                 X['execution_id'], X['source'].capitalize(), ''])
    else:
        none_row[len(none_row) - 2] = current_type
        my_writer.writerow(none_row)


def mark(my_writer, my_img, none_row, current_type):
    if "Human" in current_type:
        my_list = human(my_img)
    else:
        my_list = computer(my_img)

    if len(my_list) > 0:
        # creator, created_date, provenance.analysis source, computation, execution_id
        for i in my_list:
            # print(i)
            if "Human" in current_type:
                X = i['provenance']['analysis']
            else:
                X = i['analysis']
            creator = get_peep(i, X)
            created_date = get_date(i, X)

            if "computation" in X:
                current_type = X['computation'].capitalize()

            my_writer.writerow(
                [collection_name, my_img['studyid'], my_img['subjectid'], my_img['imageid'], current_type,
                 X['execution_id'], creator, created_date])
    else:
        none_row[len(none_row) - 2] = current_type
        my_writer.writerow(none_row)


def usage():
    print('Usage: ' + sys.argv[0] + ' [username] [password] [collection name | "all"]')
    exit(1)


if len(sys.argv) == 4:
    username = sys.argv[1]
    password = sys.argv[2]
    collection = sys.argv[3]
else:
    usage()

if 'all' in collection.lower():
    usage()

host = "http://quip-pathdb"
api = MyApi(host, username, password)

hasNext = True
collection_id = 0
collection_name = ''
out_dir = '/data/reports/'
everything = False
stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')

# if 'all' in collection.lower():
# everything = True
# images_url = '/listofimages?_format=json'
# lookup_table = api.get_collection_lookup_table()
# name = 'all'
# else:
everything = False
collection_id, collection_name = api.get_collection_info(collection)
if len(collection_name) == 0:
    print("Could not find collection:", collection)
    exit(1)
images_url = '/listofimages/' + str(collection_id) + '?_format=json'
name = re.sub('\W+', '', collection_name).lower()

file_name_multirow = 'annotations_' + name + '_' + stamp + '.csv'
file_name_singlerow = 'single_row_' + file_name_multirow
with open(out_dir + file_name_multirow, mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(
        ['Collection', 'Study ID', 'Subject ID', 'Image ID', 'Analysis type', 'Execution ID', 'Creator', 'Date'])

    count = 0
    while hasNext:
        url = images_url + '&page=' + str(count)
        count += 1
        response = api.get_data(url)
        if len(response) > 0:
            for r in response:
                img = {
                    "nid": r['nid'][0]['value'],
                    "imageid": r['imageid'][0]['value'],
                    "studyid": r['studyid'][0]['value'],
                    "subjectid": r['clinicaltrialsubjectid'][0]['value']
                }
                # print(img['imageid'])
                nothing_row = [collection_name, img['studyid'], img['subjectid'], img['imageid'], "placeholder", 'None']

                mark(csv_writer, img, nothing_row, "Segmentation")
                mark(csv_writer, img, nothing_row, "Human")
                heatmap(csv_writer, img, nothing_row)
                featuremap(csv_writer, img, nothing_row)
        else:
            hasNext = False

transform_to_single_row(out_dir + file_name_multirow, out_dir + file_name_singlerow)

exit(0)
