pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout Code from GitHub') {
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

        stage('Set Up Python Virtual Environment') {
            steps {
                script {
                    echo "Creating and activating virtual environment"
                    sh """
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    """
                }
            }
        }

        stage('Run Pipeline Script') {
            steps {
                script {
                    echo "Running pipeline script"
                    sh """
                        . ${VENV_DIR}/bin/activate
                        python pipeline/pipeline.py
                    """
                }
            }
        }
    }
}