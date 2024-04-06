# TODO: Complete this terraform file to setup the right configurations for Neo4j

resource "google_compute_firewall" "neo4j_firewall_rule" {
  name    = "neo4j-allow-specific-ips-on-ports"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = var.whitelisted_ports # Default Neo4j Ports for HTTP, HTTPS, and Bolt
  }

  source_ranges = var.whitelisted_ips # IP Whitelisting, change as necessary
  target_tags   = ["http-server","https-server"] # Firewall rule applies only to instances with this tag
}

resource "google_compute_instance" "neo4j_node" {
  count        = var.num_nodes # the number of instances to provision
  name         = "neo4j-node-${count.index}"
  machine_type = "e2-medium" # machine type of each node
  zone         = "europe-west9-a" # The instance zone(not the region)
  tags         = ["http-server","https-server"] # Tags to identify Neo4j instances
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11" # OS for each VM
      labels = var.common_labels # Some labels to identify the resources
    }
  }

  network_interface {
    network = "default"
    access_config {
      
    }
  }
  metadata_startup_script = <<-EOF
                              echo "Creating user ${var.username}"
                              sudo useradd -m -s /bin/bash -G sudo ${var.username}
                              echo "Setting up Neo4j"
                              # Additional setup commands for Neo4j can be added here
                              echo "Deactivating password for user ${var.username}"
                              sudo passwd -d ${var.username}
                              EOF
  metadata = {
    ssh-keys = "${var.username}:${file(var.public_key_path)}"
  }
}
