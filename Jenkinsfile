pipeline {
    agent any
    stages {
        stage('Stop') {
            steps {
                sh 'docker stop junctionx_container || true'
                sh 'docker rm -f junctionx_container || true'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t junctionx .'
            }
        }
        stage('Run') {
            steps {
                sh 'docker run -d -p 7000:7000 --name junctionx_container junctionx'
            }
        }
    }
}