import json, sys
from time import sleep

with open(sys.argv[1]) as input_data:
    input_json = json.load(input_data)

cnt = 0
total_articles = len(input_json)


for article in input_json:
    cnt += 1
    sys.stdout.write("\rFetching new Articles : " + str((cnt/total_articles)*100) + "%% Complete\n")
    sys.stdout.flush()
