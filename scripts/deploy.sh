#!/bin/bash

if [ "$#" -ne 1 ] ; then
    echo "usage: <azure-region>"
    exit 1
fi

region=$1
connect_str="neluser@nelcollector.$region.cloudapp.azure.com"

# replace the placeholder text in the template with the actual hostname of the VM
sed "s/##HOST##/$region.nelogger.xyz/g" default_template > "$region-default"

scp nginx.conf $connect_str:
scp "$region-default" $connect_str:default
scp trans.gif $connect_str:
scp index.php $connect_str:
scp collectorVM.sh $connect_str:
scp .screenrc $connect_str:
scp ../dns/dnsrecord.py ../dns/dnsserver.py ../dns/dns.txt $connect_str:

# nginx conf at: /etc/nginx/nginx.conf
# replace with our custom configs that allow POST, configures CORS, and logging
ssh $connect_str "sudo cp ~/nginx.conf /etc/nginx/nginx.conf"
ssh $connect_str "sudo cp ~/default    /etc/nginx/sites-available/default"

# clean up default index
ssh $connect_str "sudo rm -f /var/www/html/index.nginx-debian.html"
ssh $connect_str "sudo touch /var/www/html/index.html"

# set up PHP script to handle setting NEL policies on
ssh $connect_str "sudo cp ~/index.php /var/www/html"
ssh $connect_str "sudo cp ~/trans.gif /var/www/html"

ssh $connect_str "sudo service nginx restart"

echo "sleeping 5 seconds before test"
sleep 5

url="https://img.$region.nelogger.xyz/foo.png";
curl -s -o /dev/null -w "$region %{http_code}\n" $url;