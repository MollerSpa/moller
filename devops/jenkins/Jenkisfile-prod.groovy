@Library('jenkins-sharedlib')

def repo_sh = "https://github.com/MollerSpa/moller.git"
def submodule_branch = '14.0'

buildPipelineOdooSH(repo_sh: "${repo_sh}", submodule_branch: "${submodule_branch}")
