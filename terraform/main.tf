# Configuration for Terraform engine
# Here we tell Terraform what plugins (providers) it needs to use to undertand our command
terraform {
    required_providers {
        docker = {
            source = "kreuzwerker/docker"
            version = "2.12.2"
        }
    }
}

# Connection configuration
# We tell Terraform where is Docker
# Unix socket is standard for Linux cominication
provider "docker" {
    host = "unix:///var/run/docker.sock"
}

# Virtual network
# Creating isolated network in which our containers will live (Postgres, later Kafka etc)
# This will allow containers to talk each other by name rather than IP addresses
resource "docker_network" "crypto_network" {
    name = "crypto_network"
}

# Image definiction
# This is a "recipe" for our database downloaded from Docker Hub
resource "docker_image" "postgres_image" {
    name         = "postgres:15-alpine"
    keep_locally = true
}

# Volume (hard drive)
# Creating a permament storage space for data. Without it all crypto prices would disappear when the container is deleted
resource "docker_volume" "postgres_data" {
    name = "postgres_data"
}

# Main database container
# Here we put everything together into one working whole 
resource "docker_container" "postgres_db" {
    name  = "postgres_db"

    # REFERENCE: use image define above
    image = docker_image.postgres_image.latest

    env = [
        "POSTGRES_PASSWORD=${var.db_password}",
        "POSTGRES_USER=${var.db_user}",
        "POSTGRES_DB=crypto_db"
    ]

    # Connect to network
    networks_advanced {
        name = docker_network.crypto_network.name
    }

    # Port mapping
    ports {
        internal = 5432
        external = 5432
    }

    # Disk mounting
    # Connect the virtual disk to a specific folder within the container
    # where Postgres stores database file by default
    volumes {
        volume_name    = docker_volume.postgres_data.name
        container_path = "/var/lib/postgresql/data"
    }
}
