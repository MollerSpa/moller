
pipeline { 
    environment {
        registry = "odoopartners/odoo-sh:1.0.0"
        registryCredential = 'dockerhubtestid'
        dockerImage = ''

        repo_sh = "https://github.com/MollerSpa/moller.git"
        submodule_branch = '14.0'
    }
    agent any 
    stages { 

        stage('Preparation') {
            steps {
                script {
                    echo 'Preparing project ...'
                }
            }
        }
        stage('Pull repos') {
            steps { 
                script {
                    withCredentials([usernamePassword(credentialsId: 'odoopartnersid', passwordVariable: 'TOKEN_VALUE', usernameVariable: 'NOT_USED')]) {
                        docker.withRegistry( '', registryCredential ) {
                            sh "docker run --rm -e GIT_TOKEN=${TOKEN_VALUE} -v ${WORKSPACE}/devops/src/repos.csv:/usr/src/app/repos.csv ${registry} python ci_odoo_sh.py -u ${repo_sh} -s ${submodule_branch}"
                        }
                    }
                }
            } 
        }
        stage('Checking state') {
            steps {
                script {
                    echo 'checking state project ...'
                }
            }
        }
    }

    post {
        always {
            deleteDir()
        }
    }
}
