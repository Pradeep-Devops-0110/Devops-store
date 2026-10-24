pipeline {
  agent { label 'docker-builder' }

  stages {
    stage('Build service images') {
      steps {
        container('docker') {
          sh '''
            set -eu
            until docker info >/dev/null 2>&1; do sleep 2; done
            mkdir -p artifacts

            docker build -t local-devops/products:dev services/products
            docker build -t local-devops/orders:dev services/orders
            docker build -t local-devops/payments:dev services/payments
            docker build -t local-devops/web:dev web

            docker save -o artifacts/store-images.tar \
              local-devops/products:dev \
              local-devops/orders:dev \
              local-devops/payments:dev \
              local-devops/web:dev
          '''
        }
        archiveArtifacts artifacts: 'artifacts/store-images.tar', fingerprint: true
      }
    }
  }
}