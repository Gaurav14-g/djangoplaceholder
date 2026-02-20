pipeline {
    agent any

    stages {
    //     stage('Checkout') {
    //         steps {
    //             git 'https://github.com/Gaurav14-g/djangoplaceholder.git'
    //         }
    //     }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python manage.py test'
            }
        }

        stage('Done') {
            steps {
                echo 'CI passed. Render will auto-deploy from GitHub.'
            }
        }
    }
}