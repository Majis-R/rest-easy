pipeline {
    agent any

    environment {
        DATABASE_URL = credentials('prod-db-url')
        SECRET_KEY = credentials('prod-secret-key')
        COMMON_PASSWORD = credentials('prod-common-password')
        CORS_ORIGINS = credentials('prod-cors-origins')
        ENVIRONMENT = "production"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Dependency Check & SBOM') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate

                pip install cyclonedx-bom pip-audit

                cyclonedx-py requirements -i requirements.txt -o sbom.json

                pip-audit -r requirements.txt || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker-compose up -d --build --force-recreate
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 10
                curl -f http://localhost/health
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'sbom.json', fingerprint: true, allowEmptyArchive: true
            cleanWs()
        }
    }
}