## Elastic Stack 5.4.2 For Testing Purposes.

This docker-compose builds the elastic stack 5.4.2

Uses self signed certificate and following username and password


This stack assumes that you have got docker and docker-compose installed.

Basical steps

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update

sudo apt-get install -y docker-ce


# Install docker compose

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sysctl -w vm.max_map_count=262144


Then jsut go here --> 
https://localhost/


sudo apt-get install apache2-utils 
htpasswd -c ./app.htpasswd test

