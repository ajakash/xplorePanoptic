import json
import sys

with open("panoptic_coco_categories.json", "r") as f:
    pan = json.load(f)

with open("../coco_local/annotations/panoptic_train2017.json", "r") as f:
    data = json.load(f)

print_gen_info = False
print_category_count = False
print_label_set_samples = True

if print_gen_info:
    print len(pan)
    #for cat in pan:
    #    print cat["supercategory"], cat["name"]

    sups = {x["supercategory"] for x in pan}

    print sups, len(sups)

    cats = [(x["supercategory"], x["name"], x["isthing"]) for x in pan]

    cats = sorted(cats, key= lambda x: x[0])

    for cat in cats:
        print cat

# create category dictionary
cd = {}
for cat in pan:
    cd[cat["id"]] = {"name":cat["name"], "parent":cat["supercategory"], "count": 0, "thing?":cat["isthing"]}

ann_stats = {}
if print_category_count:
    print data.keys()

    print data["annotations"][0].keys()

    for item in data["annotations"]:
        #ann_stats[item["image_id"]] = {(x["category_id"],
        #                                cd[x["category_id"]]["name"],
        #                                cd[x["category_id"]]["parent"]) for x in item["segments_info"]}

        ann_stats[item["image_id"]] = {x["category_id"] for x in item["segments_info"]}

        for index in list(ann_stats[item["image_id"]]):
            cd[index]["count"] += 1

        #print list(sorted(ann_stats[item["image_id"]]))

        #raw_input()

    for key, val in sorted(cd.iteritems(), key=lambda (k,v): (v["count"],k)):
        print  '{} \t {} \t {:<20} \t {:<20} \t {}'.format(key, val["count"], val["name"], val["parent"], val["thing?"])

    print "There are %d images in the dataset" % len(data["annotations"])

if print_label_set_samples:
    print data.keys()
    print data["annotations"][0].keys()

    for item in data["annotations"]:
        label_set = {cd[x["category_id"]]["name"] for x in item["segments_info"]}

        print label_set
        raw_input()