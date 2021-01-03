# TooonieBox
Dies ist eine einfache version einer Tooniebox. 
## Vorbereitung
Benötigt wird ein Raspberry Pi mit Python 3, ein MFRC522, der per SPI angeschlossen ist, und einige RFID-Chips.
Zum Installieren bitte den folgenden Kommandos ausführen:

```wget -O - "https://raw.githubusercontent.com/Squeesyy/TooonieBox/main/TooonieBox/setup.sh" | sudo bash```

Das Skript wird alle benötigten Dependencies installieren, und automatische Updates mithilfe von cron durchführen. Diese werden um 9 Uhr morgens erfolgen, woaufhin der Pi einmal neustarten wird. 
Dabei werden auch die aktuellsten Dateien aus dem GitHub Repo mithilfe von git heruntergeladen, was auch die Audiodateien beinhaltet.

## Verwendung
Einfach wie eine Tooniebox. Zum Pausieren muss die Figur vom Leser genommen werden.

## Hinzufügen von Titeln
Die Datei, die hochgeladen wird, kann eintweder eine MP3 oder OGG sein. Unterstützung für MP3s ist limitiert und kann auf machen Systemen zu Problemen führen. 
Zum hinzufügen von Titeln bitte das Skript 'addTitle.py' ausführen, **nachdem** die zugehörige Audiodatei in den Order 'Musik' verschoben wurde. 
Wenn man das Skript ausführt, wird man gebeten, den exakten Dateinamen einzugeben (Bitte zwischen Groß- und Kleinbuchstaben unterscheiden, und die Dateiendung mit eingeben!). 
Danach hat man eine Minute Zeit, um den RFID-Chip aufzulegen.
Wenn ein schon vergebener Chip verwendet wird, bekommt dieser einfach eine neue Datei zugeordnet, und die zugehörige Timestamp gelöscht.
