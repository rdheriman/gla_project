pipeline {
    agent any

    triggers {
        githubPush()
    }

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timestamps()

        buildDiscarder(
            logRotator(
                numToKeepStr: '20',
                artifactNumToKeepStr: '10'
            )
        )
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
                script {
                    sh '''
                        mkdir -p backend/test-results

                        rm -f backend/test-results/pytest.xml

                        docker rm -f \
                            "reservation-pytest-${BUILD_NUMBER}" \
                            2>/dev/null || true
                    '''

                    def testStatus = sh(
                        returnStatus: true,
                        script: '''
                            docker compose \
                                --profile ci \
                                run \
                                --name "reservation-pytest-${BUILD_NUMBER}" \
                                --no-deps \
                                backend-ci \
                                uv run pytest \
                                --junitxml=/app/pytest.xml
                        '''
                    )

                    sh '''
                        docker cp \
                            "reservation-pytest-${BUILD_NUMBER}:/app/pytest.xml" \
                            backend/test-results/pytest.xml \
                            || true

                        docker rm -f \
                            "reservation-pytest-${BUILD_NUMBER}" \
                            || true
                    '''

                    junit(
                        testResults: 'backend/test-results/pytest.xml',
                        allowEmptyResults: false
                    )
                    archiveArtifacts(
                        artifacts: 'backend/test-results/pytest.xml',
                        fingerprint: true
                    )

                    if (testStatus != 0) {
                        error(
                            'Les tests backend ont échoué.'
                        )
                    }
                }
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
        stage('Deploy') {
            steps {
                echo 'Déploiement de la nouvelle version...'

                sh '''
                    docker compose \
                        -p reservation-prod \
                        up \
                        -d \
                        --build \
                        --wait \
                        --wait-timeout 120 \
                        --remove-orphans \
                        postgres backend frontend
                '''
            }
        }
        stage('Verify Deployment') {
            steps {
                sh '''
                    docker compose \
                        -p reservation-prod \
                        ps
                '''

                sh '''
                    docker compose \
                        -p reservation-prod \
                        exec -T backend \
                        python -c \
                        "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())"
                '''
            }
        }
        stage('Build Information') {
            steps {
                sh '''
                    cat > build-info.txt <<EOF
        Job: $JOB_NAME
        Build: $BUILD_NUMBER
        Commit: $(git rev-parse HEAD)
        Branch: $(git rev-parse --abbrev-ref HEAD)
        Date: $(date -Iseconds)
        EOF
                '''

                archiveArtifacts(
                    artifacts: 'build-info.txt',
                    fingerprint: true
                )
            }
        }
    }


    post {

        always {
            sh '''
                docker compose \
                    -p "$COMPOSE_PROJECT_NAME" \
                    --profile ci \
                    down \
                    -v \
                    --remove-orphans \
                    || true
            '''
        }

        success {
            echo 'CI/CD terminé avec succès.'
        }

        failure {
            echo 'Le pipeline CI/CD a échoué.'
        }
    }
}