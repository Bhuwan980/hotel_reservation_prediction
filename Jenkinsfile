pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout GitHub repo to Jenkins') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github_token',
                        url: 'https://github.com/Bhuwan980/hotel_reservation_prediction'
                    ]]
                )
            }
        }

        stage('Install Python (if needed)') {
            steps {
                sh '''
                sudo apt-get update && apt-get install -y python3 python3-pip python3-venv
                '''
            }
        }

        stage('Set up Virtual Environment') {
            steps {
                script {
                    echo "Setting up virtual environment"
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}