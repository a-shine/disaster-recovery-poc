provider "google" {
  project = var.gcp_project_id
  region  = var.region
}

# Create the Virtual Private Cloud (VPC) network and subnet for the VM's network interface
resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-mode-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "default" {
  name          = "my-custom-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

# Create a single Compute Engine instance
resource "google_compute_instance" "default" {
  name         = "non-critical-app-vm"
  machine_type = "e2-medium"
  zone         = var.zone
  tags         = ["non-critical", "ssh"] # if non-critical + same machine type as critical workload which will be replacing then replace

  # TODO: reservation affinity vs. specific reservation

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11" # TODO: use the custome image containing the OS and application
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.default.id

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}

resource "google_compute_firewall" "ssh" {
  name = "allow-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.vpc_network.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_firewall" "flask" {
  name    = "flask-app-firewall"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }
  source_ranges = ["0.0.0.0/0"]
}
