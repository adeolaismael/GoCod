output "mongo_instance_ips" {
  value = google_compute_instance.mongo_node.*.network_interface.0.access_config.0.nat_ip
}

output "mongo_ssh_commands" {
  value = [for instance in google_compute_instance.mongo_node : "ssh ${var.username}@${instance.network_interface.0.access_config.0.nat_ip}"]
}

output "neo4j_instance_ips" {
  value = google_compute_instance.neo4j_node.*.network_interface.0.access_config.0.nat_ip
}

output "neo4j_ssh_commands" {
  value = [for instance in google_compute_instance.neo4j_node : "ssh ${var.username}@${instance.network_interface.0.access_config.0.nat_ip}"]
}
