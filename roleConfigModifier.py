# Script to modify configuration for yarn role config group

import cm_client
import argparse
from pydash import _

CM_CLIENT_USERNAME = 'admin'
CM_CLIENT_PASSWORD = 'admin'
API_PROTOCOL = 'http'
API_HOST ='10.209.239.13'
PORT = '7180'
API_VERSION='v17'
CLUSTER='cluster'
SERVICE='yarn'

def configurationArg(s):
    pConfig = s.split(':')
    if len(pConfig) == 2 or len(pConfig) == 3:
        return pConfig
    else:
        raise argparse.ArgumentTypeError(s + " Invalid Format for configuration option.")

parser = argparse.ArgumentParser("Script to modify configuration for yarn role config group", conflict_handler="resolve")

parser.add_argument("-t", "--config", help="[required] Format: <config>:<value>:<?role_config_group> [The config name and it's value to set.]", action='append', type=configurationArg, required=True)
parser.add_argument("-v", "--verbose", help="[optional] Verbose", action="store_true")
parser.add_argument('--protocol', nargs='?', help="[optional] Protocol to use, Default:" + API_PROTOCOL, default = API_PROTOCOL)
parser.add_argument('--port', nargs='?', help="[optional] Port for CM API server, Default:" + PORT, default = PORT)
parser.add_argument('-h', '--host', nargs='?', help="[optional] Host IP for CM API server, Default:" + API_HOST, default = API_HOST)
parser.add_argument('--apiver', nargs='?', help="[optional] API version to use, Default:" + API_VERSION, default = API_VERSION)
parser.add_argument('-c', '--cluster', nargs='?', help="[optional] Cluster Name, Default:" + CLUSTER, default = CLUSTER)
parser.add_argument('-u', '--user', nargs='?', help="[optional] CM Client User Name, Default:" + CM_CLIENT_USERNAME, default = CM_CLIENT_USERNAME)
parser.add_argument('-p', '--password', nargs='?', help="[optional] CM Client User Password, Default:" + CM_CLIENT_PASSWORD, default = CM_CLIENT_PASSWORD)

args = parser.parse_args()

cm_client_username = args.user
cm_client_password = args.password
api_protocol = args.protocol
api_host = args.host
port = args.port
api_version = args.apiver
cluster = args.cluster
service = SERVICE

cm_client.configuration.username = cm_client_username
cm_client.configuration.password = cm_client_password

url = api_protocol + "://" + api_host + ":" + port + "/api/" + api_version

api_client = cm_client.ApiClient(url)

role_config_group_resource_api = cm_client.RoleConfigGroupsResourceApi(api_client)

config_by_roles = role_config_group_resource_api.read_role_config_groups(cluster_name=cluster, service_name=service)

config_by_group = {}
for item in config_by_roles.items:
    role_group_name = item.name
    for subitem in item.config.items:
        _.set(config_by_group, "" + subitem.name, _.push(_.get(config_by_group, "" + subitem.name, []), role_group_name))

for config in args.config:
    picked_role_config_group = None
    configuration = _.replace(config[0], '.', '_')
    value = config[1]
    specified_role_config_group = _.get(config, '[2]', None)

    if configuration in config_by_group:
        structures_for_config = config_by_group[configuration]

        picked_role_config_group = specified_role_config_group or _.find(structures_for_config, lambda x: _.ends_with(x, '-BASE'))

        if _.index_of(structures_for_config, picked_role_config_group) != -1:
            # updating configuration
            print("Updating: '{configuration}' for '{picked_role_config_group}' config group")
            try:
                new_config = cm_client.ApiConfig(name=configuration, value=value)
                new_config_list = cm_client.ApiConfigList([new_config])
                res = role_config_group_resource_api.update_config(cluster_name=cluster, role_config_group_name=picked_role_config_group, service_name=service, message="", body=new_config_list)
                if (args.verbose):
                    print('Response: {res}')
                print("Updated: Configuration {configuration}' for '{picked_role_config_group}' config group")
            except ApiException as exc:
                if (args.verbose):
                    print(exc)
                print('Failed to update')
        else:
            print("{specified_role_config_group}: The specified role group is not application for the configuration")
    else:
         print("{configuration}: No such configuration exists")


