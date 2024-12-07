#!/bin/bash

# Define the target AWS VM
TARGET_USER="ubuntu"  # Default username for Ubuntu instances

# VM Details (Add more VMs as needed)
declare -A VMS
VMS["vm1"]="3.22.250.2 /home/ryan/.ssh/project-key.pem"
VMS["vm2"]="3.22.181.60 /home/ryan/.ssh/project-key.pem"
VMS["vm3"]="3.144.14.68 /home/ryan/.ssh/project-key.pem"
VMS["vm4"]="3.142.40.244 /home/ryan/.ssh/project-key.pem"

# Prompt user to select a VM
echo "Available VMs: ${!VMS[@]}"
read -p "Enter the VM name you want to connect to (e.g., vm1): " VM_NAME

# Extract IP and key for the selected VM
VM_DETAILS=${VMS[$VM_NAME]}
IFS=' ' read -r VM_IP VM_KEY <<< "$VM_DETAILS"

# Check if the VM exists
if [ -z "$VM_IP" ] || [ -z "$VM_KEY" ]; then
  echo "Invalid VM name. Please check and try again."
  exit 1
fi

# Connect to the selected VM
echo "Connecting to $VM_NAME ($VM_IP)..."
ssh -i $VM_KEY $TARGET_USER@$VM_IP
