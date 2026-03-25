terraform {
    required_providers {
        docker = {
            source = "kreuzwerker/docker"
            version = "2.12.2"
        }
    }
}

provider "docker" {
    host = "unix:///var/run/docker.sock"
}

resource "docker_network" "crypto_network" {
    name = "crypto_network"
}

# Add Docker image
resource "docker_image" "postgres_image" {
    name         = "postgres:15-alpine"
    keep_locally = true
}

# Add volume - space for data
resource "docker_volume" "postgres_data" {
    name = "postgres_data"
}

# Create Docker container
resource "docker_container" "postgres_db" {
    name  = "postgres_db"
    image = docker_image.postgres_image.latest

    env = [
        "POSTGRES_PASSWORD=${var.db_password}",
        "POSTGRES_USER=${var.db_user}",
        "POSTGRES_DB=crypto_db"
    ]

    networks_advanced {
        name = docker_network.crypto_network.name
    }

    ports {
        internal = 5432
        external = 5432
    }

    volumes {
        volume_name    = docker_volume.postgres_data.name
        container_path = "/var/lib/postgresql/data"
    }
}
