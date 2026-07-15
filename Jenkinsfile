// Jenkinsfile
// Place this at the repo root (same level as astrology_agent/ and astrology-agent-ui/).
//
// What this pipeline does:
//   1. Checks out the repo
//   2. Creates a Python venv and installs backend dependencies
//   3. Runs the pytest suite and publishes JUnit-format results to Jenkins
//   4. Installs frontend dependencies and builds the React app
//
// In Jenkins: New Item -> Pipeline -> Pipeline script from SCM -> point at
// this repo -> Script Path: Jenkinsfile

pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend: Setup venv') {
            steps {
                dir('astrology_agent') {
                    bat '''
                        py -m venv venv
                        call venv\\Scripts\\python.exe -m pip install --upgrade pip
                        call venv\\Scripts\\pip.exe install -r requirements.txt
                    '''
                }
            }
        }

        stage('Backend: Run Tests') {
            steps {
                dir('astrology_agent') {
                    bat '''
                        call venv\\Scripts\\pytest.exe tests --junitxml=test-results.xml -v
                    '''
                }
            }
            post {
                always {
                    junit 'astrology_agent/test-results.xml'
                }
            }
        }

        stage('Frontend: Install & Build') {
            steps {
                dir('astrology-agent-ui') {
                    bat '''
                        npm install
                        npm run build
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Build succeeded: tests passed and frontend built cleanly.'
        }
        failure {
            echo 'Build failed — check the stage logs above for details.'
        }
        always {
            // Clean up the venv/build folders so the next run starts fresh
            bat '''
                if exist astrology_agent\\venv rmdir /s /q astrology_agent\\venv
            '''
        }
    }
}
