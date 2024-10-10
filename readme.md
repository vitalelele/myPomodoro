# myPomodoro 🍅

myPomodoro è un'applicazione desktop sviluppata in Python che utilizza la tecnica del Pomodoro per aiutarti a migliorare la tua produttività. Con un'interfaccia utente semplice e intuitiva, puoi gestire facilmente le tue sessioni di lavoro e le pause.

## Caratteristiche

- **Timer Pomodoro**: Imposta un timer per 25 minuti di lavoro ininterrotto.
- **Pause**: Dopo ogni sessione di lavoro, prendi una pausa di 5 minuti.
- **Cicli**: Completa un numero personalizzabile di cicli di lavoro e pause.
- **Audio**: Notifiche sonore al termine di ogni sessione.
- **Interfaccia Personalizzabile**: Scegli tra diverse durate di lavoro, pause e cicli.
- **Tema scuro/chiaro**: Passa facilmente tra la modalità scura e chiara.

## Tecnologie utilizzate

- Python
- CustomTkinter (per l'interfaccia utente)
- Pygame (per la gestione del suono)

## Installazione

Per eseguire myPomodoro, assicurati di avere Python installato sulla tua macchina. Puoi installare le dipendenze necessarie utilizzando `pip`.

1. **Clona il repository**:
   ```bash
   git clone https://github.com/vitalelele/myPomodoro.git
   ```

2. **Naviga nella directory del progetto**:
   ```bash
   cd myPomodoro
   ```

3. **Installa le dipendenze**:
   ```bash
   pip install customtkinter pygame
   ```

4. **Assicurati di avere il file audio**: 
   Scarica un file audio di notifica (es. `bell_sound.mp3`) e posizionalo nella stessa directory del file `pomodoro.py`.

5. **Esegui l'app**:
   ```bash
   python pomodoro.py
   ```

## Utilizzo

1. Avvia l'app e imposta il timer per la sessione di lavoro.
2. Clicca su "Avvia" per iniziare il timer.
3. Dopo ogni sessione di lavoro, una finestra di messaggio ti notificherà di prendere una pausa.
4. Personalizza le impostazioni attraverso il pulsante delle impostazioni per modificare la durata delle sessioni di lavoro e pause, e il numero di cicli.
   
## Contribuire

Se desideri contribuire a myPomodoro, segui questi passi:

1. Fai un fork del progetto.
2. Crea un nuovo branch per la tua feature:
   ```bash
   git checkout -b my-feature
   ```
3. Apporta le tue modifiche e aggiungi i file modificati:
   ```bash
   git add .
   ```
4. Fai un commit delle tue modifiche:
   ```bash
   git commit -m "Aggiunta di una nuova feature"
   ```
5. Fai il push delle tue modifiche:
   ```bash
   git push origin my-feature
   ```
6. Crea una nuova Pull Request.

## Licenza

Questo progetto è sotto la licenza MIT.
