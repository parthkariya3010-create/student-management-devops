
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub'
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Check Docker') {
            steps {
                bat 'docker --version'
            }
        }

        stage('Check Docker Compose') {
            steps {
                bat '"C:\\Users\\parth\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" version'
            }
        }

        stage('Build Application') {
            steps {
                bat '"C:\\Users\\parth\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" build'
            }
        }
    }
}
