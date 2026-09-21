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
                script {
                    if (isUnix()) {
                        sh "docker build -t ${DOCKER_IMAGE} ."
                    } else {
                        bat "docker build -t ${DOCKER_IMAGE} ."
                    }
                }
            }
        }
        stage('Smoke Test') {
            steps {
                script {
                    if (isUnix()) {
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
                    } else {
                        bat '''
                            docker run -d --rm --name %APP_NAME%-test -p 8501:8501 %DOCKER_IMAGE%
                            powershell -NoProfile -Command "$deadline = (Get-Date).AddSeconds(60); do { try { $response = Invoke-WebRequest -UseBasicParsing http://localhost:8501/_stcore/health; if ($response.StatusCode -eq 200) { exit 0 } } catch {} Start-Sleep -Seconds 2 } while ((Get-Date) -lt $deadline); exit 1"
                            docker stop %APP_NAME%-test
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                environment name: 'DEPLOY_TO_K8S', value: 'true'
            }
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            kubectl apply -f k8s/deployment.yaml
                            kubectl set image deployment/titanic-streamlit titanic-streamlit=${DOCKER_IMAGE}
                            kubectl rollout status deployment/titanic-streamlit --timeout=120s
                        '''
                    } else {
                        bat '''
                            kubectl apply -f k8s\deployment.yaml
                            kubectl set image deployment/titanic-streamlit titanic-streamlit=%DOCKER_IMAGE%
                            kubectl rollout status deployment/titanic-streamlit --timeout=120s
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (isUnix()) {
                    sh 'docker rm -f ${APP_NAME}-test || true'
                } else {
                    bat "docker rm -f ${APP_NAME}-test || exit 0"
                }
            }
        }
        success {
            echo "Pipeline succeeded: ${DOCKER_IMAGE}"
        }
        failure {
            echo 'Pipeline failed. Check logs above for details.'
        }
    }
}
