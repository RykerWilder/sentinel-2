
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
  "Esegui Script 1"
  "Esegui Script 2"
  "Esegui Script 3"
  "Esegui Script 4"
  "Esegui nmap"
  "Esegui Wireshark"
  "Esci"
)

select opt in "${options[@]}"; do
  case $opt in
    "Esegui Script 1")
      python moduli/cve_hunter.py
      ;;
    "Esegui Script 2")
      python moduli/ip_globetracker.py
      ;;
    "Esegui Script 3")
      python moduli/script3.py
      ;;
    "Esegui Script 4")
      python moduli/script4.py
      ;;
    "Esegui nmap")
      echo "Esecuzione di nmap..."
      nmap -v
      ;;
    "Esegui Wireshark")
      echo "Esecuzione di Wireshark..."
      wireshark
      ;;
    "Esci")
      echo "Uscita..."
      break
      ;;
    *)
      echo "Scelta non valida!"
      ;;
  esac
done
