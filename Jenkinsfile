pipeline {
    agent any

    environment {
        DATABASE_URL = credentials('prod-db-url')
        SECRET_KEY = credentials('prod-secret-key')
        COMMON_PASSWORD = credentials('prod-common-password')
        CORS_ORIGINS = credentials('prod-cors-origins')
        ENVIRONMENT = "production"
        SSL_EMAIL = credentials('ssl_email')
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
                docker-compose down --remove-orphans || true
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

        stage('Provision SSL Certificates') {
            steps {
                echo 'Checking and provisioning SSL certificate if needed...'
                sh """
                # We use --keep-until-expiring so it gracefully skips if a valid certificate is already present
                docker-compose run --rm certbot certonly \\
                  --webroot -w /var/www/certbot \\
                  --email ${SSL_EMAIL} \\
                  -d bubly.duckdns.org \\
                  --agree-tos --no-eff-email \\
                  --keep-until-expiring || true
                  
                # Reload Nginx so it starts using the newly acquired certificate (if any)
                docker-compose exec nginx nginx -s reload || true
                """
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