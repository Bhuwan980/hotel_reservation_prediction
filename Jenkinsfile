pipeline {
    agent {
        docker {
            image 'python:3.9-slim' // Multi-arch image (supports ARM)
            args '-u root' // Needed to install system packages
        }
    }

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
                sh """
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -e .
                """
            }
        }

        stage('Run Pipeline Script') {
            steps {
                sh """
                    ${VENV_DIR}/bin/python pipeline/pipeline.py
                """
            }
        }
    }
}