provider "google" {
  project = "long-grin-378416"
  region  = "europe-west3"
}

# Create the Virtual Private Cloud (VPC) network and subnet for the VM's network interface
resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-mode-network"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "default" {
  name          = "my-custom-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "europe-west3"
  network       = google_compute_network.vpc_network.id
}

# Create a single Compute Engine instance
resource "google_compute_instance" "default" {
  name         = "flask-vm"
  machine_type = "f1-micro"
  zone         = "europe-west3-a"
  tags         = ["critical", "ssh"]

  boot_disk {
    initialize_params {
      image = "critical-app-python-debian" # TODO: use the custome image containing the OS and application
    }
  }

  # metadata_startup_script = ""


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
    ports    = ["8000"]
  }
  source_ranges = ["0.0.0.0/0"]
}

# Create an image
# Create a disk snapshot of interesting data (think about the specifics of the Inges database)
# Do I work with images + snashots
# Or just snapshots