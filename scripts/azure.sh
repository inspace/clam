#!/bin/bash

# az account list-locations to see azure regions
if [ "$#" -ne 2 ] ; then
    echo "usage: <azure-region> <vm-password>"
    echo "run 'az account list-locations' to see azure regions"
    exit 1
fi

loc=$1 #"westus"  # eastus2
resourcegroup="nel-$loc"
user="neluser"
pass=$2
hostname="nelcollector"
vmname="nelcollector"
size="Standard_B1s"

az login > /dev/null

az vm list -g $resourcegroup > /dev/null
ret=$?
if [ $ret -ne 0 ]; then
    # Create a resource group.
    az group create --name $resourcegroup --location $loc

    # Create a virtual network.
    az network vnet create --resource-group $resourcegroup --name nelVnet --subnet-name nelSubnet

    # Create a public IP address.
    az network public-ip create --resource-group $resourcegroup --name nelPublicIP --dns-name $hostname

    # Create a network security group.
    az network nsg create --resource-group $resourcegroup --name nelNetworkSecurityGroup

    # Create a virtual network card and associate with public IP address and NSG.
    az network nic create \
    --resource-group $resourcegroup \
    --name nelNic \
    --vnet-name nelVnet \
    --subnet nelSubnet \
    --network-security-group nelNetworkSecurityGroup \
    --public-ip-address nelPublicIP

    # Create a new virtual machine, this creates SSH keys if not present.
    az vm create --resource-group $resourcegroup \
                 --name $vmname \
                 --nics nelNic \
                 --image UbuntuLTS \
                 --admin-username $user \
                 --admin-password $pass \
                 --public-ip-address-dns-name $hostname \
                 --size $size

    # open ports
    az vm open-port --port 22 --resource-group $resourcegroup --name $vmname --priority 900
    az vm open-port --port 80 --resource-group $resourcegroup --name $vmname --priority 910
    az vm open-port --port 443 --resource-group $resourcegroup --name $vmname --priority 920
    az vm open-port --port 53 --resource-group $resourcegroup --name $vmname --priority 930
fi