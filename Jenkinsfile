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
                    sh 'set -e' // <-- ADDED: Exit on first error

                    echo "Installing Node.js and Newman..."
                    sh 'npm install -g newman'
                    sh 'npm install -g newman-reporter-html'

                    echo "Setting up Python environment for API in test stage..."
                    sh 'apt update'
                    sh 'apt install -y python3-venv'
                    sh 'python3 -m venv venv_test_env'
                    sh '. venv_test_env/bin/activate && pip install -r requirements.txt'

                    echo "Starting Flask API for integration tests locally (SIMULATION for CI test run)..."
                    // Use explicit path to python executable
                    sh 'nohup . venv_test_env/bin/activate && venv_test_env/bin/python app.py > api.log 2>&1 &'
                    sh 'sleep 15'
                    echo "Flask API started (attempted)."

                    echo "--- Checking directory contents for api.log ---"
                    sh 'ls -la' // <-- ADDED: List files to see if api.log exists

                    echo "--- Flask API Logs (if any) ---"
                    // Use 'cat' with '|| true' so that if api.log still doesn't exist, this step
                    // doesn't cause the entire pipeline to fail (though 'set -e' would have caught it earlier).
                    // We expect 'set -e' to fail earlier if Flask didn't start.
                    sh 'cat api.log || true'
                    echo "--- Flask API Logs End ---"

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
