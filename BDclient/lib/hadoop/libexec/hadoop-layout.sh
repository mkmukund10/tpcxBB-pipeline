# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

this="${BASH_SOURCE-$0}"
common_bin=$(cd -P -- "$(dirname -- "$this")" && pwd -P)
script="$(basename -- "$this")"
this="$common_bin/$script"

HADOOP_COMMON_DIR="./"
HADOOP_COMMON_LIB_JARS_DIR="lib"
HADOOP_COMMON_LIB_NATIVE_DIR="lib/native"
HDFS_DIR="./"
HDFS_LIB_JARS_DIR="lib"
YARN_DIR="./"
YARN_LIB_JARS_DIR="lib"
MAPRED_DIR="./"
MAPRED_LIB_JARS_DIR="lib"

HADOOP_LIBEXEC_DIR=${HADOOP_LIBEXEC_DIR:-"$common_bin/../../hadoop/libexec"}
HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-"/etc/hadoop/conf"}
HADOOP_COMMON_HOME=${HADOOP_COMMON_HOME:-"$common_bin/../../hadoop"}
HADOOP_HDFS_HOME=${HADOOP_HDFS_HOME:-"$common_bin/../../hadoop-hdfs"}
HADOOP_MAPRED_HOME=${HADOOP_MAPRED_HOME:-"$common_bin/../../hadoop-mapreduce"}
HADOOP_YARN_HOME=${HADOOP_YARN_HOME:-"$common_bin/../../hadoop-yarn"}
