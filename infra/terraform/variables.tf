variable "project" {
    description = "GCP Porject ID"
    type = string
}
variable "region" {
    description = "GCP Project Region"
    type = string
}
variable "credentials" {
    description = "GCP credentials key file JSON"
    type = string
}

variable "num_nodes" {
    description = "Number of nodes"
    type = number
}

variable "username" {
    description = "Username for the VM instances"
    type = string
  
}

variable "public_key_path" {
    description = "Path to the public SSH key"
    type = string
}

variable "whitelisted_ips" {
  description = "List of IP addresses to whitelist in the firewall"
  type        = list(string)
  default     = ["62.8.8.194","88.124.100.95"] # Default to an empty list if no IPs are provided
}

variable "whitelisted_ports" {
  description = "List of ports to whitelist in the firewall"
  type        = list(string)
  default     = ["27017", "7474", "7473", "7687"]  # Default to an empty list if no ports are provided
}

variable "common_labels" {
  type = map(string)
  default = {
    owner       = "gocod"
    deployed_by = "terraform"
  }
  description = "List of Common Labels"
}
