#!/usr/bin/env bash
# ----------------------------------------------------------------------
# Main Init Script: ruft alle Teil-Skripte nacheinander auf
# ----------------------------------------------------------------------

# Sicherstellen, dass wir im Skriptverzeichnis sind
cd "$(dirname "$0")"

# Skripte ausführbar machen
chmod +x ./01_init_project.sh
chmod +x ./02_run_.sh
chmod +x ./03_update_requirements.sh
chmod +x ./04_deactivate_venv.sh
chmod +x ./src/inkgrid_run_build.sh

