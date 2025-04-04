pipeline {
  agent any
  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/YOUR_USERNAME/uta-time-attendance.git'
      }
    }
    stage('Install Dependencies') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }
    stage('Restart App') {
      steps {
        sh 'sudo systemctl restart attendance-app'
      }
    }
  }
}

