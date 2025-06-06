pipeline {
    agent any;

    environment {
        CLUSTER = "basic-web-py"
        NAMESPACE = "web-app"
        SENDER_IMG = "kind-sender-py"
        RECEIVER_IMG = "kind-receiver-py"
    }

    stages {
        stage('Cluster configuration') {
            steps {
                sh """
                kubectl config set-context --current --namespace ${env.NAMESPACE}
                """
            }
        }
        stage("Build images") {
            steps {
                script {
                    docker.build("${env.SENDER_IMG}:latest", "-f Dockerfile.sender .")
                    docker.build("${env.RECEIVER_IMG}:latest", "-f Dockerfile.receiver .")
                }
            }
        }
        stage('Load Docker images') {
            steps {
                sh """
                kind load docker-image ${env.SENDER_IMG} --name ${env.CLUSTER}
                kind load docker-image ${env.RECEIVER_IMG} --name ${env.CLUSTER}
                """
            }
        }
        stage("Create ConfigMap for Sender") {
            steps {
                sh "kubectl create configmap sender-config --from-file=k8s/config/sender.yaml"
            }
        }
        stage("Deploy resources") {
            steps {
                sh """
                kubectl apply -f k8s/dpl/receiver-dpl.yaml
                kubectl apply -f k8s/dpl/sender-dpl.yaml
                kubectl apply -f k8s/svc/receiver-svc.yaml
                kubectl apply -f k8s/svc/sender-svc.yaml
                """
            }
        }
        stage("Check Receiver logs") {
            steps {
                sh """
                echo "Waiting 30 seconds for program to run"
                sleep 30
                POD=\$(kubectl get pods --no-headers | grep receiver | awk '{print \$1}' | head -n1)
                echo "Checking logs of pod \$POD"
                kubectl logs \$POD
                """
            }
        }
    }
}
