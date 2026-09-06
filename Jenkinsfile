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

        stage('Run Unit Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python -m pip install -r requirements.txt'
                        sh 'pytest -q'
                    } else {
                        bat '''
                            @echo off
                            REM Check for python or py launcher
                            where python >nul 2>&1
                            if %ERRORLEVEL% NEQ 0 (
                                where py >nul 2>&1
                                if %ERRORLEVEL% NEQ 0 (
                                    echo ERROR: Python not found on PATH. Install Python or configure PATH.
                                    exit /b 1
                                )
                            )

                            REM Try py launcher first, fall back to python
                            py -3 -m pip install -r requirements.txt || python -m pip install -r requirements.txt
                            py -3 -m pytest -q || python -m pytest -q
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker build -t ${DOCKER_IMAGE} ."
                    } else {
                        bat 'echo Skipping Docker build on Windows agent'
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
                        bat 'echo Skipping Smoke Test on Windows agent'
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
