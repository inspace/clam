#!/bin/bash

# az account list-locations to see azure regions
if [ "$#" -ne 2 ] ; then
    echo "usage: <azure-region> <vm-password>"
    echo "run 'az account list-locations' to see azure regions"
    exit 1
fi

region=$1
password=$2

# provision VM with password. it will have a hostname of the form nelcollector.$region.cloudapp.azure.com
./azure.sh $region $password

connect_str="neluser@nelcollector.$region.cloudapp.azure.com"

# copy ssh public key to make life better.
ssh-copy-id -i ~/.ssh/id_rsa.pub $connect_str

# replace the placeholder text in the template with the actual hostname of the VM
sed "s/##HOST##/$region.nelogger.xyz/g" default_template > "$region-default"

./deploy.sh $region
# scp nginx.conf $connect_str:
# scp "$region-default" $connect_str:default
# scp trans.gif $connect_str:
# scp index.php $connect_str:
# scp collectorVM.sh $connect_str:
# scp ~/.screenrc $connect_str:
# scp dns/dnsrecord.py dns/dnsserver.py dns/dns.txt $connect_str:

ssh $connect_str "sudo ./collectorVM.sh $region"