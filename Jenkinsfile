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

        stage('Install Python and pip') {
            steps {
                script {
                    echo "Installing Python and pip if needed"
                    sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-pip python3-venv
                    '''
                }
            }
        }

        stage('Set up Virtual Environment') {
            steps {
                script {
                    echo "Setting up virtual environment"
                    // Create the virtual environment
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    '''
                }
            }
        }

        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                script {
                    echo "Activating virtual environment and installing dependencies"
                    sh '''
                    # Activate the virtual environment and install dependencies
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}