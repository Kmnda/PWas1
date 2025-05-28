pipeline {
    agent any

    stages {
        // ... (Build Flask API stage) ...

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
                    sh 'apt update'
                    sh 'apt install -y python3-venv'
                    sh 'python3 -m venv venv_test_env'
                    sh '. venv_test_env/bin/activate && pip install -r requirements.txt'

                    echo "Starting Flask API for integration tests locally (SIMULATION for CI test run)..."
                    sh 'nohup . venv_test_env/bin/activate && python app.py > api.log 2>&1 &'
                    sh 'sleep 15' // Increased sleep time
                    echo "Flask API started."
                    sh 'cat api.log' // <-- ADDED THIS LINE
                    echo "--- Flask API Logs End ---" // <-- ADDED THIS LINE

                    echo "Running Postman integration tests with Newman..."
                    sh "newman run \"Flask API Integration Tests.postman_collection.json\" -e \"Local Flask API.postman_environment.json\" --reporters cli,json,html --reporter-html-export newman-report.html --reporter-json-export newman-report.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'newman-report.html, newman-report.json', fingerprint: true
                    sh "kill \$(lsof -t -i:${API_PORT}) || true"
                    echo "Flask API process stopped."
                }
                failure {
                    echo 'Integration tests failed!'
                }
                success {
                    echo 'Integration tests passed!'
                }
            }
        }
    }
}
