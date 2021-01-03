# TooonieBox
Dies ist eine einfache version einer Tooniebox. 
## Vorbereitung
Benötigt wird ein Raspberry Pi 3 mit Python, ein MFRC522, der per SPI angeschlossen ist, und einige RFID-Chips.
Zum Installieren bitte den folgenden Kommandos ausführen:
```wget -O - "https://raw.githubusercontent.com/Squeesyy/TooonieBox/main/TooonieBox/setup.sh" | sudo bash```
Das Skript wird alle benötigten Dependencies installieren, und automatische Updates mithilfe von cron durchführen. Diese werden um 9 Uhr morgens erfolgen, woaufhin der Pi einmal neustarten wird. 
Dabei werden auch die aktuellsten Dateien aus dem GitHub Repo mithilfe von git heruntergeladen, was auch die Audiodateien beinhaltet.

## Verwendung
Einfach wie eine Tooniebox. Zum Pausieren muss die Figur vom Leser genommen werden.
