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

        stage('Install venv Support') {
            steps {
                sh """
                    apt-get update && apt-get install -y python3-venv
                """
            }
        }

        stage('Clean Previous venv') {
            steps {
                sh "rm -rf ${VENV_DIR}"
            }
        }

        stage('Set Up Python Virtual Environment') {
            steps {
                script {
                    echo "Creating and activating virtual environment"
                    sh """
                        /usr/bin/python3 -m venv ${VENV_DIR}
                        ${VENV_DIR}/bin/pip install --upgrade pip
                        ${VENV_DIR}/bin/pip install -e .
                    """
                }
            }
        }

        stage('Run Pipeline Script') {
            steps {
                script {
                    echo "Running pipeline script"
                    sh """
                        ${VENV_DIR}/bin/python pipeline/pipeline.py
                    """
                }
            }
        }
    }
}