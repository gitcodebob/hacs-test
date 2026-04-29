# Home Battery Control

A [HACS](https://hacs.xyz/) custom integration for [Home Assistant](https://www.home-assistant.io/) that provides control and automation for home battery systems.

This project is the next major iteration of [gitcodebob/marstek-venus-rs485-node-red](https://github.com/gitcodebob/marstek-venus-rs485-node-red) ([docs](https://docs.homebatterycontrol.com/)). Often shortened to 'HBC'.

## Features

- Manage and monitor your home battery from within Home Assistant
- Installable via HACS for easy setup and updates

## Installation

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.
2. Add this repository as a custom repository in HACS.
3. Search for **Home Battery Control** and install it.
4. Restart Home Assistant.

## Requirements

- Home Assistant
- HACS

## Dev container

The repo ships with a VS Code dev container that runs Home Assistant and Node-RED side by side. Node-RED cannot be installed as an HA Add-on here because the dev container uses the bare HA Container image (no Supervisor).

After "Reopen in Container":

- Home Assistant: <http://localhost:8123>
- Node-RED: <http://localhost:1880>

On first boot Node-RED runs `npm install` against [.devcontainer/nodered-data/package.json](.devcontainer/nodered-data/package.json) and pulls in `node-red-contrib-home-assistant-websocket`. Tail `docker compose logs nodered` to watch — it can take 1-2 minutes.

### Connect Node-RED to Home Assistant

1. In HA, go to your user profile -> Security -> Long-Lived Access Tokens, create a token, copy it.
2. In Node-RED, drop any `home-assistant` node onto a flow, open the server config node:
   - Base URL: `http://ha-dev:8123` (use the compose service name from inside the Node-RED container, not `localhost`)
   - Access Token: paste the LLAT
3. Deploy. The node should report "Connected".

### Importing baseline flows

Open the predecessor's `project/hbc/node-red/all-flows-in-one-file.json`, copy its contents, then in Node-RED use the hamburger menu -> Import -> paste -> Import. Flows persist in [.devcontainer/nodered-data/](.devcontainer/nodered-data/) across rebuilds.
