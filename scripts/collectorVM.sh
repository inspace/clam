#!/bin/bash

# This script assumes that 4 files have been uploaded to the users home directory
# nginx.conf, default, index.php, trans.gif
if [ "$#" -ne 1 ] ; then
    echo "usage: <azure-region>"
    exit 1
fi

region=$1

#install nginx and php module
sudo apt-get update
sudo apt-get install nginx php-fpm -y

# nginx conf at: /etc/nginx/nginx.conf
# replace with our custom configs that allow POST, configures CORS, and logging
sudo cp ~/nginx.conf /etc/nginx/nginx.conf
sudo cp ~/default    /etc/nginx/sites-available/default

# clean up default index
sudo rm -f /var/www/html/index.nginx-debian.html
sudo touch /var/www/html/index.html

# set up PHP script to handle setting NEL policies on 
sudo cp ~/index.php /var/www/html
sudo cp ~/trans.gif /var/www/html

# Create letsencrypt cert
# from https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx

sudo apt-get update
sudo apt-get install software-properties-common -y
sudo add-apt-repository universe -y
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update

#Install Certbot
sudo apt-get install certbot python-certbot-nginx -y

# Run certbot with --manual for wildcard generation with DNS-01 challenge
# (https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx and https://certbot.eff.org/docs/using.html#manual)
sudo certbot certonly --force-interactive --manual --agree-tos -m crawlder@gmail.com -d *.$region.nelogger.xyz
# sudo certbot certonly --manual
# specify wildcard domain, set DNS TXT record as instructed (not sure how to automate this)

# restart nginx
sudo service nginx restart