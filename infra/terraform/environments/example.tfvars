# GCP Project ID
project = "gocod-405620"

# GCP Project Region
region = "europe-west9" # This one is Paris

# GCP Credentials Key File JSON
credentials = "keys\gcpkey.json"

# Number of nodes 
num_nodes = 2

# Path to the public SSH key
public_key_path = "keys\id_rsa.pub"

# List of IP addresses to whitelist in the firewall
whitelisted_ips = ["0.0.0.0/0"]

# List of ports to whitelist in the firewall
whitelisted_ports = ["0-65535"] #allow traffic on all ports

# List of Common Labels
common_labels = {
  owner       = "gocod"
  deployed_by = "terraform"
}

# Username for the VM instances(this one is replaced by the script init-deploy.sh)
username = "izaga_admin"
