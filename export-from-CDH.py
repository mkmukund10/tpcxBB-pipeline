import cm_client
from cm_client.rest import ApiException
from collections import namedtuple
from pprint import pprint
import json

# Configure HTTP basic authorization: basic
cm_client.configuration.username = 'admin'
cm_client.configuration.password = 'admin'

api_url = "http://10.209.239.13:7180/api/v17"
api_client = cm_client.ApiClient(api_url)

# create an instance of the API class
cluster_name = 'Cluster 1' # str |
clusters_api_instance = cm_client.ClustersResourceApi(api_client)
template = clusters_api_instance.export(cluster_name)

# Following step allows python fields with under_score to map
# to matching camelCase name in the API model before writing to json file.
json_dict = api_client.sanitize_for_serialization(template)
with open('/home/tpc/hs/tpcxBB-pipeline/13sep-2019-cluster_template.json', 'w') as out_file:
    json.dump(json_dict, out_file, indent=4, sort_keys=True)
