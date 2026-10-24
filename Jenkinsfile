
pipeline {
  agent any

  stages {
    stage('Check project files') {
      steps {
        sh 'test -f services/products/app.py'
        sh 'test -f services/orders/app.py'
        sh 'test -f services/payments/app.py'
        sh 'test -f web/index.html'
        echo 'Storefront and service source files are present.'
      }
    }
  }
}
