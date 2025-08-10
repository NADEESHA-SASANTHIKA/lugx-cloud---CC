pipeline {
  agent {label 'master'}
  environment {
    // Change namespace if your deployments are in a different one
    KUBE_NAMESPACE = 'default'
  }
  stages {
    stage('Get current color') {
      steps {
        script {
          def active = sh(script: "kubectl get svc game-service -o jsonpath='{.spec.selector.version}' --namespace ${env.KUBE_NAMESPACE}", returnStdout: true).trim()
          echo "game-service active version: ${active}"
        }
      }
    }
    stage('Deploy new images to inactive') {
      steps {
        script {
          def services = ['game-service','order-service','analytics-service','frontend']
          for (s in services) {
            def active = sh(script: "kubectl get svc ${s} -o jsonpath='{.spec.selector.version}' --namespace ${env.KUBE_NAMESPACE}", returnStdout: true).trim()
            if (active == '') {
              echo "Service ${s} has no version selector; skipping"
              continue
            }
            def inactive = (active == 'blue') ? 'green' : 'blue'
            echo "Updating image for ${s} -> deployment ${s}-${inactive}"
            sh "kubectl set image deployment/${s}-${inactive} ${s}=nadeesha171/${s}:latest --namespace ${env.KUBE_NAMESPACE}"
            sh "kubectl rollout status deployment/${s}-${inactive} --namespace ${env.KUBE_NAMESPACE} --timeout=120s"
          }
        }
      }
    }
    stage('Integration tests (against new inactive pods)') {
      steps {
        script {
          sh '''
            kubectl run curl-test --rm -i --restart=Never --image=curlimages/curl --namespace ${KUBE_NAMESPACE} -- \
              sh -c "curl -f http://game-service:5000/games || exit 1; curl -f http://order-service:5001/orders || exit 1; curl -f http://frontend:80/shop.html || exit 1"
          '''
        }
      }
    }
    stage('Switch traffic to new version') {
      steps {
        script {
          def services = ['game-service','order-service','analytics-service','frontend']
          for (s in services) {
            def active = sh(script: "kubectl get svc ${s} -o jsonpath='{.spec.selector.version}' --namespace ${env.KUBE_NAMESPACE}", returnStdout: true).trim()
            if (active == '') {
              echo "Service ${s} has no version selector; skipping"
              continue
            }
            def newver = (active == 'blue') ? 'green' : 'blue'
            echo "Switching ${s} selector to version=${newver}"
            sh "kubectl patch svc ${s} -p '{\"spec\":{\"selector\":{\"app\":\"${s}\",\"version\":\"${newver}\"}}}' --namespace ${env.KUBE_NAMESPACE}"
          }
        }
      }
    }
  }
  post {
    success {
      echo "Blue-Green deployment finished successfully."
    }
    failure {
      echo "Pipeline failed. Do not switch traffic — investigate and rollback if necessary."
    }
  }
}
