pipeline {
    agent any
    stages {
        stage('Run') {
            steps {
                sh 'python3 deploy_container.py ' + env.BRANCH_NAME
            }
        }
    }
}