## Elastic Stack 5.4.2 For Testing Purposes.

This docker-compose builds the elastic stack 5.4.2

Uses self signed certificate and out of the box elastic passwords 

username: elastic
password: changeme

To change the username and password

####First ensure that you have apache-utils installed

sudo apt-get install apache2-utils

#### run the below command in the ./my-nginx directory

htpasswd -c ./app.htpasswd <newusername>


This stack assumes that you have got docker and docker-compose installed.

Basical steps to get docker and docker-compose installed

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update

sudo apt-get install -y docker-ce

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

##NOTE host needs to have the following set or elasticsearch will not boot
sysctl -w vm.max_map_count=262144

##TO run

Clone the repo and then run docker-compose up

Elasticsearch will be running here --> 
https://localhost/

Kibana will be running here -->
https://localhost/kibana


sudo apt-get install apache2-utils 
htpasswd -c ./app.htpasswd test

