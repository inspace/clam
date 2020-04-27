#install nginx
sudo apt-get update
sudo apt-get install nginx -y

# nginx conf at: /etc/nginx/nginx.conf




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
sudo certbot certonly --manual
# specify wildcard domain, set DNS TXT record as instructed (not sure how to automate this)


#- Congratulations! Your certificate and chain have been saved at:
#   /etc/letsencrypt/live/kyriakoszarifis.com/fullchain.pem
#   Your key file has been saved at:
#   /etc/letsencrypt/live/kyriakoszarifis.com/privkey.pem
#   Your cert will expire on 2020-07-19. To obtain a new or tweaked
#   version of this certificate in the future, simply run certbot
#   again. To non-interactively renew *all* of your certificates, run
#   "certbot renew"


# tell nginx to use listen on 443 and use the new cert:
# add the following to /etc/nginx/sites-available/default
server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name <example.com> <www.example.com>;
    ssl_certificate <path_to_fullchain_pem>;
    ssl_certificate_key <path_to_privkey_pem>;

    root /var/www/example.com/html;
    index index.html index.htm index.nginx-debian.html;

}


# tell nginx to allow POST

# add .php that dumps POST payload to a file

# restart nginx
sudo service nginx restart
