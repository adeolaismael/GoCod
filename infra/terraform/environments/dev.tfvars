# GCP Project ID
project = "gocod-405620"

# GCP Project Region
region = "europe-west9" # This one is Paris

# GCP Credentials Key File JSON
credentials = "/workspace/keys/gcpkey.json"

# Number of nodes 
num_nodes = 2

# Path to the public SSH key
public_key_path = "/home/devcontainer/.ssh/id_rsa.pub"

# List of IP addresses to whitelist in the firewall
whitelisted_ips = ["62.8.8.194","88.124.100.95"]

# List of ports to whitelist in the firewall
whitelisted_ports = ["27017", "7474", "7473", "7687"] #allow traffic on all ports

# List of Common Labels
common_labels = {
  owner       = "gocod"
  deployed_by = "terraform"
}

# Username for the VM instances(this one is replaced by the script init-deploy.sh)
username = "admin"
