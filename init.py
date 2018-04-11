import json
import os, json
import errno
import csv
import pandas as pd
from pandas.io.json import json_normalize
from pprint import pprint
# import cric_regression as cr
path_to_json = '/home/dheeraj/Desktop/odis/'
path_to_cleaned_json = '/home/dheeraj/Desktop/odis/cleaned_data/'
path_to_csv='/home/dheeraj/Desktop/odis/cleaned_csv/'
def aggregate(f):
	tot_runs = 0
	tot_wickets = 0
	over = -1
	runs = []
	wickets = []
	data = json.load(open(path_to_json+f))
	bat_team = data["innings"][0]["1st innings"]["team"]
	for i in range(51):
		runs.append(0)
		wickets.append(0)
	for i in range (0,len(data["innings"][0]["1st innings"]["deliveries"])):
	 	ball = list(data["innings"][0]["1st innings"]["deliveries"][i].values())
	 	if(over<float(list(data["innings"][0]["1st innings"]["deliveries"][i].keys())[0])):
	 		over+=1
	 	runs[over]=tot_runs
	 	runs[over]+=ball[0]["runs"]["batsman"]+ball[0]["runs"]["extras"]
	 	tot_runs+=ball[0]["runs"]["batsman"]+ball[0]["runs"]["extras"]
	 	if ("wicket" in ball[0]):
	 		tot_wickets+=1
	 	wickets[over]=tot_wickets
	final_score=str(tot_runs)+"/"+str(tot_wickets)
	#json create
	jdata = {}
	jdata['bat_team']=bat_team
	jdata['scores_by_overs']={}
	over_stat = []
	for i in range(1,51):
		over_stat.append({'over':i, 'runs':runs[i],'wickets':wickets[i]})
		jdata['scores_by_overs']=over_stat
# print(over_stat)
	jdata['tot_runs']=tot_runs
	jdata['tot_wickets']=tot_wickets
	jdata['final_score']=final_score
	jdata['venue']=data["info"]["venue"]
	if("city" in data["info"]):
		jdata['city']=data["info"]["city"]

	filename = path_to_cleaned_json+jdata['bat_team']+'/'+f
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	with open(path_to_cleaned_json+jdata['bat_team']+'/'+f, 'w') as c:
		json.dump(jdata, c,indent=4,sort_keys=True)
		print("Useful Match. Aggregated and saved as "+jdata['bat_team']+'/'+f)
	result = json_normalize(jdata,'scores_by_overs',['bat_team','tot_runs','tot_wickets','city','venue','final_score'],errors='ignore')
	# result = result.drop(result.columns[0],axis=1)
	filename = path_to_csv+jdata['bat_team']+'/'+f+".csv"
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	result.to_csv(path_to_csv+jdata['bat_team']+'/'+f+".csv")
	print("Saved as "+jdata['bat_team']+'/'+f+".csv")
	return

c1 = 0
c2 = 0
not_useful = []
useful = []
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for i in json_files:
	data = json.load(open(path_to_json+i))
	c1+=1
	if ("winner" not in data["info"]["outcome"]):
		c2+=1
		print(i+" : Match abandoned/interrupted by rain. Data not useful")
		not_useful.append(i)
		continue
	last_ball = float(list(data["innings"][0]["1st innings"]["deliveries"][-1:][0].keys())[0])
	# print(last_ball)
	if (last_ball<49.6):
		not_useful.append(i)
		print(i + ": 1st innings less than 50 overs. Data not useful")
		continue
	useful.append(i)
	# Aggregation and jsonify
	aggregate(i)

print(c1)
print(len(not_useful))

#Merge all cleaned CSV into one file
subfolders = [f.name for f in os.scandir(path_to_csv) if f.is_dir() ]
for subfolder in subfolders:
	print(subfolder)
	os.chdir(path_to_csv+subfolder)
	dfs = [pd.read_csv(f) for f in os.listdir(os.getcwd())]
	finaldf = pd.concat(dfs, axis=0, join='inner')
	finaldf.to_csv(subfolder+".csv")
	print(finaldf)
	print("All data contatenated and saved into one csv file: +"+subfolder+".csv")