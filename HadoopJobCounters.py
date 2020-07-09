import requests
import json
import csv
import sys

class JobMetrics:
    def __init__(self, jobCounterName='', jobMapCounterValue=0, jobReduceCounterValue=0, jobTotalCounterValue=0):
        self.jobCounterName = jobCounterName
        self.jobMapCounterValue = jobMapCounterValue
        self.jobReduceCounterValue = jobReduceCounterValue
        self.jobTotalCounterValue = jobTotalCounterValue


#job = JobMetrics()
#print (job.jobTotalCounterValue)

# open a file for writing
hadoop_file = ''

#list containign started job_ids
jobId = []

dict_job_metrics = {}

def aggregateJobCounters(job_id):
    url = "http://bdw21-13:19888/ws/v1/history/mapreduce/jobs/"+job_id+"/counters"
    #print url
    header = []
    values = []
    response = requests.get(url)
    if(response.ok):
        jData = json.loads(response.content)
        jobCounters = jData['jobCounters']
        #print jobCounters
        header.append('id')
        values.append(jobCounters['id'])
        counterGroup = jobCounters['counterGroup']
        #print counterGroup
        #counter = counterGroup['counter']
        #print counter
        for group in counterGroup:
            counter = group['counter']
            #print counter
            for count in counter:
                name = count['name']
                mapCounterValue = count['mapCounterValue']
                reduceCounterValue = count['reduceCounterValue']
                totalCounterValue = count['totalCounterValue']
                if name in dict_job_metrics.keys():
                    j_obj = dict_job_metrics[name]
                    #print j_obj.jobCounterName, j_obj.jobMapCounterValue
                    j_obj.jobMapCounterValue = j_obj.jobMapCounterValue + mapCounterValue
                    j_obj.jobReduceCounterValue = j_obj.jobReduceCounterValue + reduceCounterValue
                    j_obj.jobTotalCounterValue = j_obj.jobTotalCounterValue + totalCounterValue
                    #print j_obj.jobCounterName, j_obj.jobMapCounterValue
                else:
                    j_obj = JobMetrics(name, mapCounterValue, reduceCounterValue, totalCounterValue)
                    dict_job_metrics[name] = j_obj
    else:
        response.raise_for_status()


def writeToCsv():
    global hadoop_file
    #print hadoop_file
    jobData = open(hadoop_file+'--hadoopCounters.csv', 'w')
    # create csv writer
    csvwriter = csv.writer(jobData)
    header = []
    values = []
    for key in dict_job_metrics.keys():
        header.append(key+'_mapCounterValue')
        header.append(key+'_reduceCounterValue')
        header.append(key+'_totalCounterValue')
        j_obj = dict_job_metrics[key]
        values.append(j_obj.jobMapCounterValue)
        values.append(j_obj.jobReduceCounterValue)
        values.append(j_obj.jobTotalCounterValue)
    csvwriter.writerow(header)
    csvwriter.writerow(values)

def parseJobId(logFile):
    global hadoop_file
    hadoop_file = logFile.split('.')[0]
    #print hadoop_file
    with open(logFile, 'r') as file:
        for line in file:
            if 'Starting Job' in line:
                jId = line.split(',')[0].split('=')[1]
                jobId.append(jId[1:])
                print jId[1:]


def callAggregation():
    for item in jobId:
        aggregateJobCounters(item)

parseJobId(sys.argv[1])

callAggregation()

writeToCsv()
