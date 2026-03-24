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
