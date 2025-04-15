pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout github repo to jenkins') {
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

        stage('setting up virtual env'){
            steps{
                scripts{
                    echo "setting up venv"
                    sh '''
                    pyhton -m venv - ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    
                    '''

                }
            }
        }

    }
}