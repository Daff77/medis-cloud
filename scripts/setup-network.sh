#!/usr/bin/env bash
set -e

echo ">>> Memeriksa Docker Network 'medis-net'..."
if docker network ls --format '{{.Name}}' | grep -wq '^medis-net$'; then
    echo "Docker network 'medis-net' sudah ada."
else
    echo "Membuat custom bridge network 'medis-net'..."
    docker network create --driver bridge medis-net
fi

echo ">>> Detail Jaringan 'medis-net':"
docker network inspect medis-net --format 'Subnet: {{range .IPAM.Config}}{{.Subnet}}{{end}}'
