pipeline {
    agent any
    stages{
        stage('Checkout the code'){
            steps{
                git branch: 'main', url: 'https://github.com/trdevops146/practice-project-2.git'
            }
        }
        stage('Build the docker image'){
            steps{
                sh '''
                sudo apt update
                docker build -t trdevops/python-app:api-service -f ./api-service/Dockerfile ./api-service
                docker build -t trdevops/python-app:frontend-service -f ./frontend-service/Dockerfile ./frontend-service
                '''
            }
        }
        stage('Login to Dockerhub and push the image to Dockerhub'){
            steps{
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                sh '''
                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                docker push trdevops/python-app:api-service
                docker push trdevops/python-app:frontend-service
                '''
                }

            }
        }
        stage('Deploy the kubernetes artifacts into the minikube cluster'){
            steps{
                withCredentials([string(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_CONTENT')]) {
                    sh '''
                    echo "$KUBECONFIG_CONTENT" > kubeconfig
                    export KUBECONFIG=kubeconfig
                    kubectl get pods
                    '''
                }
            }
        }
    }
}