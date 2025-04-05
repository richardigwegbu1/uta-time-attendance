pipeline {
  agent any

  stages {
    stage('Clone') {
      steps {
        git branch: 'main', url: 'https://github.com/richardigwegbu1/uta-time-attendance.git'
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

