import pymongo

host = 'ca-mongo'
my_client = pymongo.MongoClient("mongodb://" + host + ":27017/")
my_db = my_client["camic"]
heat_col = my_db['heatmap']
mark_col = my_db['mark']


def get_data(query, collection):
    my_set = set()
    for x in collection.find(query, {
        "provenance.analysis.execution_id": 1,
        "_id": 0
    }):
        my_set.add(x['provenance']['analysis']['execution_id'])
    return my_set


def segmentations(nid, imageid, studyid, subjectid):
    return get_data({
        "provenance.image.slide": str(nid),
        "provenance.image.imageid": imageid,
        "provenance.image.study": studyid,
        "provenance.image.subject": subjectid
    }, mark_col)


def heatmaps(nid, imageid, studyid, subjectid):
    return get_data({
        "provenance.image.slide": str(nid),
        "provenance.image.subject_id": subjectid,
        "provenance.image.case_id": imageid,
        "provenance.analysis.study_id": studyid
    }, heat_col)
