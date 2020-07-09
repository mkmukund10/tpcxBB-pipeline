pipeline {
    agent any

    parameters {
         string(name: 'hiveDatabase', defaultValue: 'bbench100', description: 'TPCxBB hive databse name')
         string(name: 'DataEngine', defaultValue: 'hive', description: 'Data processing engine hive or spark')
         string(name: 'ScaleFactor', defaultValue: '100', description: 'TPCx-BB dataset size')
         string(name: 'mapTasks', defaultValue: '432', description: 'No of map tasks')
         string(name: 'streams', defaultValue: '10', description: 'No of parallel queries to run: #streams')
         string(name: 'benchmarkPhase', defaultValue: 'POWER_TEST', description: 'TPCx-BB benchmark Phase to run query')
         string(name: 'QueryNo', defaultValue: '28', description: 'Single or comma separated list of queries')
         string(name: 'TuneComment', defaultValue: 'Query28-check-mapred-javaHeap2g', description: 'TPCxBB Tuning comment')
    }

    triggers {
         pollSCM('* * * * 3')
     }

stages{
        stage('Power-Phase Executions'){
           steps {
		   sh '''
		   su - root - << EOF
		   Big-Data-Benchmark-for-Big-Bench/bin/bigBench runBenchmark -d $hiveDatabase -e $DataEngine -f $ScaleFactor -m $mapTasks -s $streams -b -i $benchmarkPhase -j $QueryNo
		   '''
	}
            post {
                success {
                    echo 'Completed TPCx-BB Benchmark Phase. Copying Results.... '
                    sh '/root/Big-Data-Benchmark-for-Big-Bench/logGen.sh ${BUILD_TAG} ${TuneComment}' 
                }
            }
        }

        stage ('Analysing Results'){
            parallel{
                stage ('Generating Jupiter Notebook for Analysis'){
                    steps {
                        echo 'Jupiter Notebook Generated... Available at URL :'
                    }
                }

                stage ("Generating ML dataset with CDH configs and TPCx-BB Results"){
                    steps {
                        echo 'ML dataset generated'
                    }
                }
            }
        }
    }
}
