#!/usr/bin/env python3
#pip3 install requests
#batch5 is pipeline name in jenkins
import requests
#import subprocess

def jfrogUpload() :
    url = 'http://3.95.135.158:8082/artifactory/example-repo-local/kubernetes-configmap-reload-0.0.1-SNAPSHOT.jar'
    file_path = '/var/lib/jenkins/workspace/batch5/target/kubernetes-configmap-reload-0.0.1-SNAPSHOT.jar'
    username = 'admin'
    password = 'Euro@2023'

    with open(file_path, 'rb') as file:
        response = requests.put(url, auth=(username, password), data=file)  
        
        if response.status_code == 201:
          print("\nPut request was succesfull")
        else:
            print("PUT request failed with status code (response.status_code)")
            print("Response content:")
            print(response.txt)


jfrogUpload()
