#!/bin/bash
# ============================================================
# Open WebUI Docker Backup Script
# Run this directly on the Raspberry Pi (or any Docker host)
#
# Usage:
#   chmod +x backup-openwebui.sh
#   ./backup-openwebui.sh
#
# What it backs up:
#   1. Container filesystem (app code, configs, installed packages)
#   2. Docker volume data (database, uploads, settings, chat history)
#   3. Container metadata (image, env vars, ports, volumes)
# ============================================================

set -e

# Configuration
BACKUP_DIR="$HOME/openwebui-backup-$(date +%Y%m%d_%H%M%S)"
CONTAINER_NAME=""

echo "============================================"
echo "  Open WebUI Docker Backup"
echo "============================================"
echo ""

# Step 1: Find the Open WebUI container
echo "[1/6] Finding Open WebUI container..."

# Try common container names
for name in "open-webui" "openwebui" "open_webui"; do
    if docker ps --format '{{.Names}}' | grep -q "^${name}$"; then
        CONTAINER_NAME="$name"
        break
    fi
done

# If not found by name, search by image
if [ -z "$CONTAINER_NAME" ]; then
    CONTAINER_NAME=$(docker ps --format '{{.Names}}\t{{.Image}}' | grep -i "open-webui\|openwebui" | head -1 | cut -f1)
fi

# If still not found, list all containers and ask
if [ -z "$CONTAINER_NAME" ]; then
    echo ""
    echo "Could not auto-detect Open WebUI container."
    echo "Running containers:"
    docker ps --format "  {{.Names}} ({{.Image}})"
    echo ""
    read -p "Enter the container name: " CONTAINER_NAME
fi

if [ -z "$CONTAINER_NAME" ]; then
    echo "ERROR: No container name provided. Exiting."
    exit 1
fi

# Verify container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "ERROR: Container '${CONTAINER_NAME}' is not running."
    echo "Running containers:"
    docker ps --format "  {{.Names}} ({{.Image}})"
    exit 1
fi

echo "  Found container: ${CONTAINER_NAME}"

# Step 2: Create backup directory
echo "[2/6] Creating backup directory: ${BACKUP_DIR}"
mkdir -p "$BACKUP_DIR"

# Step 3: Save container metadata
echo "[3/6] Saving container metadata..."
docker inspect "$CONTAINER_NAME" > "$BACKUP_DIR/container-inspect.json"

# Save the image name
CONTAINER_IMAGE=$(docker inspect --format='{{.Config.Image}}' "$CONTAINER_NAME")
echo "$CONTAINER_IMAGE" > "$BACKUP_DIR/image-name.txt"
echo "  Image: ${CONTAINER_IMAGE}"

# Save volume mounts info
echo "  Volume mounts:"
docker inspect --format='{{range .Mounts}}  {{.Type}}: {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' "$CONTAINER_NAME"
docker inspect --format='{{json .Mounts}}' "$CONTAINER_NAME" > "$BACKUP_DIR/volume-mounts.json"

# Step 4: Export container filesystem
echo "[4/6] Exporting container filesystem (this may take a while)..."
docker export "$CONTAINER_NAME" > "$BACKUP_DIR/container-filesystem.tar"
CONTAINER_SIZE=$(du -sh "$BACKUP_DIR/container-filesystem.tar" | cut -f1)
echo "  Container filesystem: ${CONTAINER_SIZE}"

# Step 5: Backup Docker volumes
echo "[5/6] Backing up Docker volumes..."

# Get all volume mounts
VOLUMES=$(docker inspect --format='{{range .Mounts}}{{if eq .Type "volume"}}{{.Name}} {{end}}{{end}}' "$CONTAINER_NAME")

if [ -n "$VOLUMES" ]; then
    for vol in $VOLUMES; do
        echo "  Backing up volume: ${vol}"
        # Use a temporary container to tar the volume contents
        docker run --rm \
            -v "${vol}:/volume-data:ro" \
            -v "$BACKUP_DIR:/backup" \
            alpine \
            tar cf "/backup/volume-${vol}.tar" -C /volume-data .
        VOL_SIZE=$(du -sh "$BACKUP_DIR/volume-${vol}.tar" | cut -f1)
        echo "    Size: ${VOL_SIZE}"
    done
else
    echo "  No named volumes found."
fi

# Also backup bind mounts (if any)
BIND_MOUNTS=$(docker inspect --format='{{range .Mounts}}{{if eq .Type "bind"}}{{.Source}}:{{.Destination}} {{end}}{{end}}' "$CONTAINER_NAME")

if [ -n "$BIND_MOUNTS" ]; then
    echo "  Backing up bind mounts..."
    BIND_COUNT=0
    for mount in $BIND_MOUNTS; do
        SRC=$(echo "$mount" | cut -d: -f1)
        DST=$(echo "$mount" | cut -d: -f2)
        BIND_COUNT=$((BIND_COUNT + 1))
        SAFE_NAME=$(echo "$DST" | tr '/' '_' | sed 's/^_//')
        echo "    ${SRC} -> ${DST}"
        if [ -d "$SRC" ]; then
            tar cf "$BACKUP_DIR/bind-mount-${SAFE_NAME}.tar" -C "$SRC" .
            BIND_SIZE=$(du -sh "$BACKUP_DIR/bind-mount-${SAFE_NAME}.tar" | cut -f1)
            echo "      Size: ${BIND_SIZE}"
        else
            echo "      WARNING: Source path does not exist or is not a directory"
        fi
    done
fi

# Step 6: Create summary
echo "[6/6] Creating backup summary..."

TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

cat > "$BACKUP_DIR/BACKUP-INFO.txt" << EOF
============================================
  Open WebUI Docker Backup
============================================

Date:       $(date '+%Y-%m-%d %H:%M:%S %Z')
Container:  ${CONTAINER_NAME}
Image:      ${CONTAINER_IMAGE}
Host:       $(hostname)
Total Size: ${TOTAL_SIZE}

Files:
$(ls -lh "$BACKUP_DIR" | tail -n +2)

To restore:
  1. Create a new container from the image:
     docker pull ${CONTAINER_IMAGE}
     docker run -d --name ${CONTAINER_NAME} -p 3000:8080 -v open-webui-data:/app/backend/data ${CONTAINER_IMAGE}

  2. Restore volume data:
     docker stop ${CONTAINER_NAME}
     docker run --rm -v open-webui-data:/volume-data -v \$(pwd):/backup alpine sh -c "cd /volume-data && tar xf /backup/volume-*.tar"
     docker start ${CONTAINER_NAME}

  3. Or import the full container filesystem:
     docker import container-filesystem.tar open-webui-backup:local
EOF

echo ""
echo "============================================"
echo "  Backup Complete!"
echo "============================================"
echo ""
echo "  Location: ${BACKUP_DIR}"
echo "  Total size: ${TOTAL_SIZE}"
echo ""
echo "  Files:"
ls -lh "$BACKUP_DIR"
echo ""
echo "  To copy to another machine:"
echo "    scp -r ${BACKUP_DIR} user@remote:~/backups/"
echo ""
