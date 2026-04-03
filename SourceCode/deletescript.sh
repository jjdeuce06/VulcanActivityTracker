#!/bin/bash

RG="vulcan-rg"

echo "Deleting resource group $RG and all contained resources..."
az group delete --name $RG --yes --no-wait
echo "Resource group deletion started. It may take a few minutes."