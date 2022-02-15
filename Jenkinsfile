pipeline {
  agent any
  tools {
    maven 'Maven'
  }
  stages {
    stage ('Initialize') {
      steps {
        sh '''
                    echo "PATH = ${PATH}"
                    echo "M2_HOME = ${M2_HOME}"
            ''' 
      }
    }
    
    stage ('Build') {
      steps {
      sh 'mvn clean package'
       }
    }
    
    stage ('Dependency Check') {
      steps {
        dependencyCheck additionalArguments: '''
              -f "XML"''', odcInstallation: 'Dependency-Check'
        dependencyCheckPublisher pattern: 'dependency-check-report.xml'
	      }
    }
    
    stage ('Upload Reports to Defect Dojo') {
	 steps {
		withDockerContainer(image: 'python:3'){
			withEnv(["HOME=${env.WORKSPACE}"]) {
				withCredentials([string(credentialsId: 'api_key', variable: 'KEY'), string(credentialsId: 'defect_host', variable: 'DEFECT_HOST')]) {
					sh 'cat $HOME/dependency-check-report.xml'
					sh 'python -m pip install requests'
					sh 'JOB_NAME=$env.JOB_NAME'
					sh 'chmod +x upload-files.py'
					sh 'python upload-files.py --host $DEFECT_HOST --api_key $KEY --name $JOB_NAME --result_file $HOME/dependency-check-report.xml --scanner "Dependency Check Scan"'
				}
			}
		}
	}
    }
    
    stage ('Deploy-To-Tomcat') {
            steps {
		    withCredentials([string(credentialsId: 'tomcat_host', variable: 'TOMCAT_HOST')]) {
           		sshagent(['tomcat']) {
                		sh 'scp -o StrictHostKeyChecking=no target/*.war ubuntu@$TOMCAT_HOST:/home/ubuntu/apache-tomcat-8.5.75/webapps/webapp.war'
		    	}
		   }      
           }       
    }
       
    }
      
}
