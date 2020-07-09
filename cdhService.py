import sys
import cm_client
from cm_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basic
cm_client.configuration.username = 'admin'
cm_client.configuration.password = 'admin'

#Service required print statement
#print "Enter service required:cluster/Spark/HDFS/YARN(MR2 Included)/Hive/ZooKeeper as first argument"

# Create an instance of the API class
api_host = 'http://10.209.239.13'
port = '7180'
api_version = 'v17'

# Construct base URL for API
# http://cmhost:7180/api/v30
api_url = api_host + ':' + port + '/api/' + api_version
api_client = cm_client.ApiClient(api_url)
cluster_api_instance = cm_client.ClustersResourceApi(api_client)

# Lists all known clusters.
api_response = cluster_api_instance.read_clusters(view='SUMMARY')
for cluster in api_response.items:
    print cluster.name,"-", cluster.full_version

# Below is obtained as first args of this program : Service to restart
#Srv="Spark"
#Srv=sys.argv[1]

if cluster.full_version.startswith("5."):
    services_api_instance = cm_client.ServicesResourceApi(api_client)
    services = services_api_instance.read_services(cluster.name, view='FULL')
    for service in services.items:
        print service.display_name, "-", service.type
#        if service.type == Srv:
        if service.type == "HDFS":
            hdfs = service
