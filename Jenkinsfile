pipeline {
    agent any

    environment {
        APP_NAME = 'titanic-streamlit'
        IMAGE_TAG = "${env.BUILD_NUMBER ?: 'local'}"
        DOCKER_IMAGE = "${APP_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    docker run -d --rm --name ${APP_NAME}-test -p 8501:8501 ${DOCKER_IMAGE}
                    python - <<'PY'
import time
import urllib.request
import sys

url = 'http://localhost:8501/_stcore/health'
for _ in range(30):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            print('Health check status:', response.status)
            sys.exit(0)
    except Exception:
        time.sleep(2)
print('Health check failed')
sys.exit(1)
PY
                    docker stop ${APP_NAME}-test
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f ${APP_NAME}-test || true'
        }
        success {
            echo "Pipeline succeeded: ${DOCKER_IMAGE}"
        }
        failure {
            echo 'Pipeline failed. Check logs above for details.'
        }
    }
}
