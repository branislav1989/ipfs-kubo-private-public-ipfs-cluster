#!/usr/bin/env bash
# Usage: init_kubo_node.sh /var/lib/ipfs/private <optional-swarm-key-path>
set -euo pipefail
repo_path="$1"
swarm_key="${2:-}"

mkdir -p "$repo_path"
chown -R root:root "$repo_path"

export IPFS_PATH="$repo_path"
if [ ! -d "$IPFS_PATH/config" ]; then
  ipfs init
  echo "Initialized ipfs repo at $IPFS_PATH"
else
  echo "Repo already initialized at $IPFS_PATH"
fi

if [ -n "$swarm_key" ] && [ -f "$swarm_key" ]; then
  cp -f "$swarm_key" "$IPFS_PATH/swarm.key"
  chmod 400 "$IPFS_PATH/swarm.key"
  echo "Installed swarm.key"
fi

echo "Done. You can now start the ipfs daemon with systemd or manually."
