
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

        stage('Run Automated Tests') {
            steps {
                bat 'python -m unittest discover -s tests -v'
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

        stage('Deploy Application') {
            steps {
                bat '"C:\\Users\\parth\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" up -d'
            }
        }

        stage('Health Check') {
            steps {
                bat 'python -c "import urllib.request; r=urllib.request.urlopen(\'http://localhost:5000/health\', timeout=10); print(r.read().decode()); assert r.status == 200"'
            }
        }
    }
}
