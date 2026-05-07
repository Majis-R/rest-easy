pipeline {
    agent any

    triggers {
        // Triggers the pipeline when a push to the repository occurs
        // (Requires GitHub webhook configured in Jenkins)
        githubPush()
    }

    environment {
        // You would typically map your Jenkins credentials to environment variables here
        // DATABASE_URL = credentials('prod-db-url')
        // SECRET_KEY = credentials('prod-secret-key')
        // COMMON_PASSWORD = credentials('prod-common-password')
        // CORS_ORIGINS = credentials('prod-cors-origins')
        // ENVIRONMENT = "production"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Dependency Check & SBOM') {
            steps {
                echo 'Generating Software Bill of Materials (SBOM)...'
                // Create a virtual environment for the build tools
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                
                # Install CycloneDX for SBOM generation and pip-audit for vulnerability checking
                pip install cyclonedx-bom pip-audit
                
                # Generate a CycloneDX SBOM from requirements.txt
                cyclonedx-py requirements -i requirements.txt -o sbom.json
                
                # Optional: Run a vulnerability scan on dependencies
                pip-audit -r requirements.txt || echo "WARNING: Vulnerabilities found!"
                '''
            }
        }

        stage('Build Image') {
            steps {
                echo 'Building Docker container...'
                sh 'docker compose build --no-cache'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                // Spin up securely using variables injected by the environment block
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            // Archive the generated SBOM so it can be downloaded from the Jenkins UI
            archiveArtifacts artifacts: 'sbom.json', fingerprint: true, allowEmptyArchive: true
            
            // Clean up workspace after build
            cleanWs()
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed. Please check the logs.'
        }
    }
}