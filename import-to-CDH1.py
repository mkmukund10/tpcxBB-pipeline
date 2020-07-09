import cm_client
from cm_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basic
cm_client.configuration.username = 'admin'
cm_client.configuration.password = 'admin'

# Create an instance of the API class
api_host = 'http://10.209.239.13'
port = '7180'
api_version = 'v17'

api_url = api_host + ':' + port + '/api/' + api_version
api_client = cm_client.ApiClient(api_url)

role_config_group_resource = cm_client.RoleConfigGroupsResourceApi(api_client)

node_manager_base_config = role_config_group_resource.read_config("cluster", "yarn-NODEMANAGER-BASE", "yarn")

#for configItem in node_manager_base_config.items:
#    print(configItem.name + ": " + configItem.value);

new_config = cm_client.ApiConfig(name="yarn_nodemanager_resource_memory_mb", value="262144")
new_config_list = cm_client.ApiConfigList([new_config])
res = role_config_group_resource.update_config("cluster", "yarn-NODEMANAGER-BASE", "yarn", message="",body=new_config_list)
res = role_config_group_resource.update_config("cluster", "yarn-NODEMANAGER-1", "yarn", message="",body=new_config_list)
res = role_config_group_resource.update_config("cluster", "yarn-NODEMANAGER-2", "yarn", message="",body=new_config_list)
