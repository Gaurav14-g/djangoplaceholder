pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                bat 'python --version'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Clean Old Migrations (CI only)') {
            steps {
                echo 'Removing old migration files (except __init__.py)'
                bat '''
for /r %%d in (migrations) do (
    if exist "%%d" (
        del /q "%%d\\*.py"
        del /q "%%d\\*.pyc"
        echo cleaned %%d
    )
)
'''
            }
        }

        stage('Make Migrations') {
            steps {
                bat 'python manage.py makemigrations'
            }
        }

        stage('Migrate') {
            steps {
                bat 'python manage.py migrate'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python manage.py test'
            }
        }

        stage('Done') {
            steps {
                echo 'CI passed: migrations + migrate + tests successful.'
            }
        }
    }
}