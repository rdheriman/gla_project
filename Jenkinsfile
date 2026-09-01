pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        COMPOSE_PROJECT_NAME =
            "reservation-ci-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }


        stage('Build CI Images') {
            steps {
                sh '''
                    docker compose \
                        --profile ci \
                        build backend-ci frontend-ci
                '''
            }
        }


        stage('Backend Lint') {
            steps {
                sh '''
                    docker compose \
                        --profile ci \
                        run --rm --no-deps \
                        backend-ci \
                        uv run ruff check .
                '''

                sh '''
                    docker compose \
                        --profile ci \
                        run --rm --no-deps \
                        backend-ci \
                        uv run ruff format --check .
                '''
            }
        }


        stage('Test Database') {
            steps {
                sh '''
                    docker compose \
                    --profile ci \
                    up -d --wait postgres-test
                '''
            }
        }


        stage('Backend Tests') {
            steps {
                sh '''
                    docker compose \
                        --profile ci \
                        run --rm \
                        backend-ci \
                        uv run pytest
                '''
            }
        }


        stage('Frontend Lint') {
            steps {
                sh '''
                    docker compose \
                        --profile ci \
                        run --rm --no-deps \
                        frontend-ci \
                        npm run lint
                '''
            }
        }


        stage('Frontend Build') {
            steps {
                sh '''
                    docker compose \
                        --profile ci \
                        run --rm --no-deps \
                        frontend-ci \
                        npm run build
                '''
            }
        }


        stage('Docker Build') {
            steps {
                sh '''
                    docker compose \
                        build backend frontend
                '''
            }
        }
    }


    post {

        always {
            sh '''
                docker compose \
                    --profile ci \
                    down -v \
                    --remove-orphans \
                    || true
            '''
        }

        success {
            echo 'Pipeline CI terminé avec succès.'
        }

        failure {
            echo 'Le pipeline CI a échoué.'
        }
    }
}