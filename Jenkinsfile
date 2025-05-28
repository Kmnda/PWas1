pipeline {
    agent any

    stages {
        stage('Build Flask API') {
            steps {
                echo "Building Flask API..."
                sh 'apt update' // Removed sudo
                sh 'apt install -y python3-venv' // Removed sudo
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        // ... (other stages) ...

        stage('Run Integration Tests') {
            environment {
                API_PORT = 5001
            }
            steps {
                script {
                    echo "Installing Node.js and Newman..."
                    sh 'npm install -g newman'
                    sh 'npm install -g newman-reporter-html'

                    echo "Setting up Python environment for API in test stage..."
                    sh 'apt update' // Removed sudo
                    sh 'apt install -y python3-venv' // Removed sudo
                    sh 'python3 -m venv venv_test_env'
                    sh 'source venv_test_env/bin/activate && pip install -r requirements.txt'

                    // ... (rest of the stage) ...
                }
            }
            // ... (post actions) ...
        }
    }
}
