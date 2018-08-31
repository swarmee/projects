## Elastic Stack 6.3.1 For Testing Purposes.

This docker-compose builds the elastic stack 6.3.1

Uses self signed certificate (so you need to click through the warning) and the following username and password

username: test
password: test

To change the username and password

## First ensure that you have apache-utils installed

```sudo apt-get install apache2-utils```

## run the below command in the ./my-nginx directory

```htpasswd -c ./app.htpasswd <newusername>```

This stack assumes that you have got docker and docker-compose installed.

## Basical steps to install docker

```curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -```

```sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"```

```sudo apt-get update```

```sudo apt-get install -y docker-ce```

## Basic Steps to Install docker-compose

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

## Map Count
Elastic will not boot up with out a increased max_map_count even in containers - so need to run the below on your host machine --> 
```sysctl -w vm.max_map_count=262144```


## Once Booted

Go here for Kibana access--> 
https://localhost/

Go here for direct elasticseach access--> 
https://localhost/search/
