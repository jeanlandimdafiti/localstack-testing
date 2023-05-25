#!/bin/bash

SAMLOCAL_CLI=$(which samlocal)
MACHINE_PYTHON=$(which python3)
MACHINE_PIP3=$(which pip3)
MACHINE_DOCKER=$(which docker)
MACHINE_DOCKER_COMPOSE=$(which docker-compose)
SUDO=
if [ ! $(id -u) -eq 0 ]; then
  SUDO=sudo
fi

install_samlocal_cli() {
  if [[ ! -f "${MACHINE_PIP3}" ]]; then
    install_pip
  fi
  echo "installing samlocal cli"
  pip3 install aws-sam-cli-local
}

install_pip() {
  if [[ ! -f "${MACHINE_PYTHON}" ]]; then
    install_python
  fi
  echo "installing pip"
  $SUDO apt install python3-pip -y

}

install_python() {
  echo "installing python3"
  $SUDO apt install python3 -y
}

if [[ ! -f "${SAMLOCAL_CLI}" ]]; then
  $SUDO apt update
  install_samlocal_cli
else
  echo "sam and samlocal is already installed, nothing to do"
fi

if [[ ! -f "${MACHINE_DOCKER}" ]]; then
  echo "Please install docker!"
  exit 1
else
  echo "docker is already installed, nothing to do"
fi

if [[ ! -f "${MACHINE_DOCKER_COMPOSE}" ]]; then
  echo "Please install docker-compose!"
  exit 1
else
  echo "docker-compose is already installed, nothing to do"
fi

echo "Done!"
