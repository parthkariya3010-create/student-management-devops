
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is managed by Jenkins SCM'
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

        stage('Build Application') {
            steps {
                bat 'docker compose build'
            }
        }
    }
}
