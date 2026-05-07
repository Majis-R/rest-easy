pipeline {
    agent any

    environment {
        DATABASE_URL = credentials('prod-db-url')
        SECRET_KEY = credentials('prod-secret-key')
        COMMON_PASSWORD = credentials('prod-common-password')
        ENVIRONMENT = "production"
        SSL_EMAIL = credentials('ssl_email')
    }

    stages {
        // stage('Checkout') {
        //     steps {
        //         checkout scm
        //     }
        // }

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

        stage('Provision SSL Certificates & Deploy') {
            steps {
                echo "Executing Let's Encrypt Initialization Script..."
                sh '''
                chmod +x init-letsencrypt.sh
                ./init-letsencrypt.sh
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