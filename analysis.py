import json

with open("simulation_results_db.json", "r") as r:
    data = json.load(r)

for run in data.keys():
    print(">>>>> Run " + str(run) +" <<<<<")
    for key in data[run].keys():
        print("\t=====" + key +"=====")
        for inner_key in data[run][key]:
            print("\t\t-----" + inner_key +"-----")
            #print(data[key][inner_key])
            print("\t\t\tduration: " + str(data[run][key][inner_key][1]- data[run][key][inner_key][0]))
            print("\t\t\tkey generated: " + str(data[run][key][inner_key][2]))