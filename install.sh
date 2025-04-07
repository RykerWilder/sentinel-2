
#!/bin/bash

set -e

# Crea un nuovo venv se non esiste già
if [ ! -d "venv" ]; then
    python3 -m venv venv || { echo "Errore nella creazione del venv"; exit 1; }
fi

# Attiva il venv
source venv/bin/activate || { echo "Errore nell'attivazione del venv"; exit 1; }

# Installa le dipendenze pip
pip install -r requirements.txt || { echo "Errore nell'installazione delle dipendenze pip"; exit 1; }

# Scarica nmap e wireshark per macOS se non sono già installati
if ! brew ls --versions nmap > /dev/null; then
    brew install nmap || { echo "Errore nell'installazione di nmap"; exit 1; }
fi

if ! brew ls --versions wireshark > /dev/null; then
    brew install wireshark --with-qt || { echo "Errore nell'installazione di wireshark"; exit 1; }
fi
