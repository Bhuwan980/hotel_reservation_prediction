pipeline {
    agent {
        docker {
            image 'python:3.9-slim-buster' // Or your preferred Python image
            args '-u root' // Run as root inside the container (be mindful of security)
        }
    }

    environment {
        VENV_DIR = '/app/venv' // Adjust path inside the container
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
                        source ${VENV_DIR}/bin/activate
                        python pipeline/pipeline.py
                    """
                }
            }
        }
    }
}