#!/usr/bin/env bash
# One-click installer for ComfyUI
# Detects package manager and installs dependencies.

set -e

log() {
  echo "[INSTALL] $1"
}

# Detect OS
if [ -f /etc/os-release ]; then
  . /etc/os-release
  DISTRO=$ID
else
  DISTRO="unknown"
fi

install_deps_apt() {
  sudo apt-get update
  sudo apt-get install -y python3 python3-venv git || return 1
}

install_deps_dnf() {
  sudo dnf install -y python3 python3-virtualenv git || return 1
}

install_deps_pacman() {
  sudo pacman -Sy --noconfirm python python-virtualenv git || return 1
}

case "$DISTRO" in
  ubuntu|debian)
    log "Using apt for installation"
    install_deps_apt || log "apt installation failed"
    ;;
  fedora|centos|rhel)
    log "Using dnf for installation"
    install_deps_dnf || log "dnf installation failed"
    ;;
  arch)
    log "Using pacman for installation"
    install_deps_pacman || log "pacman installation failed"
    ;;
  *)
    log "Unknown distro: $DISTRO. Please install Python 3, venv, and git manually."
    ;;
esac

# Create virtual environment
if [ ! -d venv ]; then
  python3 -m venv venv || { log "Failed to create virtualenv"; exit 1; }
fi

source venv/bin/activate

pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt || log "Failed to install Python dependencies"
fi

log "Installation complete. Run 'source venv/bin/activate && python main.py' to start ComfyUI"

