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
                    sh 'set -e' // Exit on first error

                    echo "Installing Node.js and Newman..."
                    sh 'npm install -g newman'
                    sh 'npm install -g newman-reporter-html'

                    echo "Setting up Python environment for API in test stage..."
                    sh 'apt update'
                    sh 'apt install -y python3-venv'
                    sh 'python3 -m venv venv_test_env'
                    sh '. venv_test_env/bin/activate && pip install -r requirements.txt'

                    echo "Attempting to start Flask API in foreground for debugging..."
                    // This is the CRITICAL line change:
                   sh 'timeout 30s . venv_test_env/bin/activate && venv_test_env/bin/python app.py > api.log 2>&1 || true'

                    echo "--- Checking directory contents for api.log ---"
                    sh 'ls -la'

                    echo "--- Flask API Startup Logs (from api.log) ---"
                    sh 'cat api.log || true'
                    echo "--- Flask API Logs End ---"

                    echo "--- Performing API health check ---"
                    sh '''
                        API_URL="http://127.0.0.1:${API_PORT}/"
                        MAX_RETRIES=10
                        RETRY_DELAY=5 # seconds

                        for i in $(seq 1 $MAX_RETRIES); do
                            echo "Attempt $i: Checking API at $API_URL"
                            if curl -s -f -o /dev/null $API_URL; then
                                echo "API is up and running!"
                                break
                            else
                                echo "API not yet ready. Waiting ${RETRY_DELAY}s..."
                                sleep $RETRY_DELAY
                            fi
                            if [ $i -eq $MAX_RETRIES ]; then
                                echo "ERROR: API did not start within the given time. Failing build."
                                exit 1
                            fi
                        done
                    '''
                    echo "--- API Health Check Complete ---"

                    echo "Running Postman integration tests with Newman..."
                    sh "newman run \"Flask API Integration Tests.postman_collection.json\" -e \"Local Flask API.postman_environment.json\" --reporters cli,json,html --reporter-html-export newman-report.html --reporter-json-export newman-report.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'newman-report.html, newman-report.json', fingerprint: true
                    // This kill command will still attempt to find and stop the process.
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
