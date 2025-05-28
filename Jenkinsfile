pipeline {
    agent any // Specifies that this pipeline can run on any available Jenkins agent

    stages {
        stage('Build Flask API') {
            steps {
                echo "Building Flask API..."
                // Use python3 if your agent has it, otherwise just 'python'
                sh 'python3 -m venv venv' // Create a virtual environment
                sh 'source venv/bin/activate && pip install -r requirements.txt' // Activate and install dependencies
            }
        }

        stage('Deploy to Staging') {
            steps {
                echo "Simulating deployment of Flask API to staging environment..."
                // IMPORTANT: In a real scenario, this would be your actual deployment logic
                echo "Flask API deployed to staging (http://your-staging-api-url:5001)"
            }
        }

        stage('Run Integration Tests') {
            environment {
                API_PORT = 5001 // Flask API port
            }
            steps {
                script {
                    echo "Installing Node.js and Newman..."
                    // Ensure Node.js is installed on your Jenkins agent.
                    // If not, you might need to add a Node.js tool configuration in Jenkins
                    // or use a Docker agent with Node.js pre-installed.
                    sh 'npm install -g newman'
                    sh 'npm install -g newman-reporter-html' // Install the HTML reporter

                    echo "Setting up Python environment for API in test stage..."
                    sh 'python3 -m venv venv_test_env' // Create a new venv for this stage
                    sh 'source venv_test_env/bin/activate && pip install -r requirements.txt'

                    // Start the Flask API in the background for local testing within Jenkins
                    // IMPORTANT: In a real CI, the API would already be deployed
                    // and running on the staging environment.
                    sh 'nohup source venv_test_env/bin/activate && python app.py > api.log 2>&1 &'
                    sh 'sleep 10' // Give Flask API time to start
                    echo "Flask API started locally for tests."

                    echo "Running Postman integration tests with Newman..."
                    // Ensure these names exactly match your files, including capitalization and spaces
                    sh "newman run \"Flask API Integration Tests.postman_collection.json\" -e \"Local Flask API.postman_environment.json\" --reporters cli,json,html --reporter-html-export newman-report.html --reporter-json-export newman-report.json"
                }
            }
            post {
                always {
                    // Archive Newman reports for later viewing in Jenkins
                    archiveArtifacts artifacts: 'newman-report.html, newman-report.json', fingerprint: true
                    // Clean up the Flask API process
                   // Kills process on port ${API_PORT}
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
