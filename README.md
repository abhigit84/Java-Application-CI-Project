steps to follow:-

stages of CI covered:

Declarative: Checkout SCM,Git Checkout,Unit Test maven,Integration Test maven,Static code analysis:Sonarqube,Quality Gate Status Check : Sonarqube,Maven Build : maven,Docker Image Build,Docker Image Scan: trivy,Docker Image Push : DockerHub	Docker Image Cleanup : DockerHub

Create ec2 instance:-
Region:us-east-1
40 gb -ebs
ubuntu-t2.xlarge
sudo su
without key proceed

Tool Installation scripts Repository:https://github.com/abhigit84/tools_installation_scripts.git

Repository on which CICD done:


https://github.com/abhigit84/Java_app_3.0.git



Shared jenkins library repo url:

https://github.com/abhigit84/jenkins_shared_lib.git

1)install jenkins(we need java for jenkins,refer github-https://github.com/abhigit84/tools_installation_scripts.git for jenkins,download package,add the lines to jenkins file,install jenkins):-

#!/bin/bash

sudo apt update -y

sudo apt upgrade -y 

sudo apt install openjdk-17-jre -y

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update -y 
sudo apt-get install jenkins -y

2)Change the security group

security groups-edit inbound rules-
add rule-all traffic-anywhere on ipv4-add rule
Now u can see 8080 port predefined.u dont have to configure port.

http://3.80.131.138:8080
this is master url

 cat /var/lib/jenkins/secrets/initialAdminPassword
put password-shown on screen
install all suggested plugins
all admin(username,password)
email
jenkins url-http://3.80.131.138:8080/
Note for jenkins login-all admin(username,password)

3)new-name-pipeline project
pipeline -definition-pipeline script from scm-SCM-git-repo url(https://github.com/abhigit84/Java_app_3.0.git)-branch specifier(*/main)

Note:-whenever any pipeline changes select that pipeline and click configure.
Also this is picking Jenkinsfile(only with this name will be picked Jenkinsfile1 will be ignored) from Github and using it in Jenkins pipeline(delarative) unline mr devops CICD Project in which he wrote scripts inside jenkins pipeline box. 

4)dahsboard-manage jenkins-plugins-available plugins-search and install all plugins in 1 go(all plugins for sonarcube and jfrog)
ManageJenkins->Plugins->Available plugins 

PluginsforSonar/Jfrog:-(select one by one and install at 1 go)
Sonar Gerrit
SonarQube Scanner
SonarQube Generic Coverage
Sonar Quality Gates 
QualityGates
Artifactory
Jfrog	

Restart jenkins option select

5)SetupDocker

refer scripts and run-
https://github.com/abhigit84/tools_installation_scripts.git for docker

docker -v


6)Install sonarcube(Port of sonarcube is 9000)

refer scripts and run-
https://github.com/abhigit84/tools_installation_scripts.git for sonarqube

 (docker run -d --name sonarqube -p 9000:9000 -p 9092:9092 sonarqube)this script writtten



7)docker ps -a
get container id -04c1cce58d3a

docker start 04c1cce58d3a

8)http://3.80.131.138:9000/

sonracube url-http://3.80.131.138:9000

login

admin
admin-change password

9)generate tokens of sonarcube for jenkins
sonar dashboard-my account-administration-security-tokens-generate token
type will be global access token
copy secret key

10)integrte sonar to jenkins
administration-configuration-webhooks

put any name and url will be below:
http://3.80.131.138:8080/sonarqube-webhook/

10)install maven

refer like above tool install scripts repo

11)install trivy (it is image security tool for image like sonarqube is for github code.it is scanning docker image)
refer like above tool install scripts repo


12)Integrate sonarqube and docker with jenkins

a)sonarqube:

jenkins dashboard-manage jenkins-configure system
ctrl f-search-sonarqube-add sonarqube-
name-sonar-api
server url--http://3.80.131.138:9000
there should be no / after 9000
if add token not coming save and come back to page again.

Click on add token->Select Secret text->Add the sonar tokenfrom step 9->Give nameof tokenas sonarqube-api

Add Token-kind(secret text)- 
copy here from step 9

id-sonarqube-api

ADD.

u can now see in server authentication token added that is -sonarqube-api-select it and save.


b)add docker hub credential id

jenkins dashboard -manage jenkins-credentials-system-click on global credentials-
add kind-use  username with password-dockerhub username-and password-id-docker-Create

13)add the jenkins shared library(this is like modules of terraform and contains many groovy script files or functions)

dashboard-manage jenkins-configure system-ctrl f(global pipeline library)-
name(my-shared-library)this is same name as mentioned in ur main Jenkinsfile otherwise will not work in github repo-default version-main
Jenkinsfile calls shared library groovy scripts which are nothing but functions like mvnbuild() etc.note mvnbuild is name of groovyfile which we call.

SCM-git-repo url-https://github.com/abhigit84/jenkins_shared_lib.git

DOCKER WE GAVE USRNAME PASSWORD UNLIKE SONAR WHERE WE GAVE SECRET TEXT.
dockerhub and sonarcube integrated..rest all tools with run only by installation on that instance without integration with jenkins(docker,maven,trivy etc)fortify we will not used as used in company enviroment

14)Now click on Jenkins job-build with parameters-dockerhubuser-should be your dockeruser id(put ur dockerhubid and not others as build will fail) as parameters its picking from Jenkinsfile of github where other user id written.
Click on Build now.

Notes:
Click on workspaces below console output-here ur code is there-u can see target folder-inside this u can see application jar which is built by maven.
this jar name coming from pom.xml 
you can also see sonarqube quality gate green button passed and passed.you can click and it takes u to sonarqube page.you can search in full output logs with quality and see quality checks ok.
you can see trivy scan giving vulnerabilities(u can copy cve and see fix for it as devsecops engineer)
