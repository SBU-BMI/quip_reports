import pymongo

host = 'ca-mongo'
my_client = pymongo.MongoClient("mongodb://" + host + ":27017/")
my_db = my_client["camic"]
heat_col = my_db['heatmap']
mark_col = my_db['mark']
analysis_col = my_db['analysis']


# SEGMENTATIONS - COMPUTER, AND HUMAN.
def computer(quad):
    # analysis. submit_date, type, computation, execution_id
    my_list = []
    exec_list = []  # weed out the duplicates

    # QUERY ON IMAGE
    query = {
        "provenance.image.slide": str(quad['nid']),
        "provenance.image.imageid": quad['imageid'],
        "provenance.image.study": quad['studyid'],
        "provenance.image.subject": quad['subjectid']
    }

    # for x in mark_col.find(query, {
    #     "geometries": 0,
    #     "_id": 0
    # }):
    for x in analysis_col.find(query, {
        "analysis": 1,
        "_id": 0
    }):
        execid = x['provenance']['analysis']['execution_id']
        if execid not in exec_list:
            exec_list.append(execid)
            my_list.append(x)

    return my_list


def human(quad):
    # creator, created_date, provenance.analysis source, computation, execution_id
    my_list = []
    exec_list = []  # weed out the duplicates

    query = {
        "provenance.image.slide": str(quad['nid']),  # "50830"
        "provenance.analysis.source": "human"
    }

    for x in mark_col.find(query, {"_id": 0, "geometries": 0}):
        execid = x['provenance']['analysis']['execution_id']
        if execid not in exec_list:
            exec_list.append(execid)
            my_list.append(x)

    return my_list


# HEATMAP
def heat(quad):
    # source, execution_id, computation (no date)
    my_list = []
    exec_list = []  # weed out the duplicates

    query = {
        "provenance.image.slide": str(quad['nid']),
        "provenance.image.case_id": quad['imageid'],
        "provenance.image.subject_id": quad['subjectid'],
        "provenance.analysis.study_id": quad['studyid']
    }

    for x in heat_col.find(query, {"_id": 0, "data": 0}):
        execid = x['provenance']['analysis']['execution_id']
        if execid not in exec_list:
            exec_list.append(execid)
            my_list.append(x)

    return my_list
