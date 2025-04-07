#!/bin/bash

# Naviga alla directory dove si trova run.sh
cd "$(dirname "$0")"

# Verifica se venv è presente
if [ ! -d "venv" ]; then
  echo "Errore: l'ambiente virtuale non è stato creato. Esegui prima 'python3 install.py'."
  exit 1
fi

# Attiva l'ambiente virtuale
echo "Attivando l'ambiente virtuale..."
source venv/bin/activate

# Mostra il menu
PS3="Scegli un'opzione: "
options=(
  "Gather software's weaknesses"
  "Gather ip information"
  "Gather sys information"
  "Run nmap"
  "Run wireshark"
  "Exit"
)

select opt in "${options[@]}"; do
  case $opt in
    "Gather software's weaknesses")
      python moduli/cve_hunter.py
      ;;
    "Gather ip information")
      python moduli/ip_globetracker.py
      ;;
    "Gather sys information")
      python moduli/sys_insider.py
      ;;
    "Run nmap")
      echo "Wait for nmap..."
      nmap -v
      ;;
    "Run wireshark")
      echo "Wait for Wireshark..."
      wireshark
      ;;
    "Exit")
      echo "Exit..."
      break
      ;;
    *)
      echo "Invalid choice!"
      ;;
  esac
done
