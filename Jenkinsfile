pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'iris-api'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo '📦 Installing dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🧪 Running tests...'
                bat 'python -m pytest tests/ -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                bat "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline succeeded!'
            echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            cleanWs()
        }
    }
}