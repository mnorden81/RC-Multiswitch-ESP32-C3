# Abnahmeprüfung RC-Multiswitch C3 und S3

Stand 28.10.2026, Firmware v4.07

Mit dieser Liste prüfst du ein fertig gebautes RC-Multiswitch C3 oder S3 mit Firmware v4.07 in 11 Schritten, vom Messen ohne Strom bis zur Modulkette. Sie ersetzt die kurze Liste in Kapitel 8 der Firmware-Spezifikation.

So gehst du vor: Schritte der Reihe nach abarbeiten, jedes Kästchen abhaken, Abweichungen in der Spalte „Notiz“ eintragen. Schlägt ein Schritt fehl, erst die Ursache klären, dann weiter. Zeilen mit „nur C3“ oder „nur S3“ beim anderen Modul überspringen.

Hinweis: Die Firmware ist bisher nur kompiliert, nicht auf echter Hardware getestet. Die erwarteten Ergebnisse stammen aus Quellcode und README.

## 1. Kopfdaten und Werkzeug

| Angabe | Eintrag |
| --- | --- |
| Modul (C3 oder S3) | |
| Platinen-Nr. / Aufbau-Nr. | |
| Firmware-Version (laut Web-UI) | |
| Werte R1-R8 (LED) und R9-R16 (Last) | |
| Datum | |
| Geprüft von | |

Du brauchst:

- Multimeter (Spannung, Durchgang, Widerstand)
- Labornetzteil mit Strombegrenzung, oder ein BEC 5 V plus Akku 2S/3S für VLOAD
- ELRS-Empfänger mit CRSF-Ausgang und gebundener Sender mit EdgeTX (ExpressLRS-Lua-Skript bzw. Geräte-Menü und das Multiswitch-Widget)
- PC mit Arduino IDE und USB-C-Kabel
- Handy oder Laptop mit WLAN
- 8 Testverbraucher, z. B. LED mit passendem Vorwiderstand oder 12-V-Glühlampe
- Optional: FrSky FLVSS/MLVSS LiPo-Sensor mit Diode 1N4148, GPS-Modul (z. B. ATGM336H), ein bis zwei weitere fertige Module für die Kette
- JST-GH-4-Kabel 1:1 für die Modulkette

## 2. Sichtprüfung und Messung ohne Strom

Alles ohne Versorgung, ESP-Board noch ohne USB.

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 2.1 | Lötstellen ansehen (Lupe), besonders ESP-Stiftleisten, ULN2803A, JST-GH-Buchsen | keine Brücken, keine kalten Lötstellen | ☐ | |
| 2.2 | Einbaurichtung prüfen: ULN2803A (Kerbe), LED1-8, TVS P6KE18A (Ring) | wie Bestückungsdruck | ☐ | |
| 2.3 | Durchgang +5 V gegen GND an CN1 (Pin 2 gegen Pin 1) | kein Kurzschluss (mehr als ca. 100 Ω) | ☐ | |
| 2.4 | Durchgang VLOAD gegen GND an CN2 | kein Kurzschluss | ☐ | |
| 2.5 | Durchgang VLOAD gegen +5 V | keine Verbindung, die zwei Netze sind getrennt | ☐ | |
| 2.6 | GND von CN1, CN2, J5 (und J6 beim S3) untereinander | Durchgang | ☐ | |
| 2.7 | CN1 Pin 3 (RX) zum ESP: C3 IO20, S3 IO44; Pin 4 (TX) zum ESP: C3 IO21, S3 IO43 | Durchgang | ☐ | |
| 2.8 | J5 Pin 3 (TX) und Pin 4 (RX): C3 IO10 / IO8, S3 IO13 / IO12 | Durchgang | ☐ | |
| 2.9 | nur S3: J6 TX IO2, RX IO1 | Durchgang | ☐ | |

## 3. Versorgung (CN1 5 V und CN2 VLOAD)

Erst Netzteil mit Strombegrenzung, dann erst Empfänger/BEC. Kein USB gesteckt, solange CN1 versorgt wird (Vorsicht, bis geklärt ist, ob das Board eine Rückstromdiode hat).

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 3.1 | 5,0 V an CN1 (Pin 2 +, Pin 1 GND), Strombegrenzung 300 mA | Stromaufnahme ohne WLAN ca. 30-80 mA, mit WLAN-AP bis ca. 150 mA (Spitzen höher); kein Strom am Limit | ☐ | |
| 3.2 | 3,3 V am 3V3-Pin des ESP-Boards messen | 3,2-3,4 V | ☐ | |
| 3.3 | 5 V an J5 Pin 2 (und J6 Pin 2 beim S3) | gleich wie CN1, für das nächste Modul | ☐ | |
| 3.4 | Keine Bauteile werden warm (Finger nach 1 min) | nichts warm | ☐ | |
| 3.5 | Jetzt zusätzlich 5 V an CN2 (VLOAD), Strombegrenzung 500 mA, alle Ausgänge aus | kaum Strom (nur Leckstrom, unter 1 mA) | ☐ | |
| 3.6 | VLOAD auf 12 V erhöhen | weiter kaum Strom, TVS bleibt kalt (P6KE18A spricht erst ab ca. 15-18 V an) | ☐ | |
| 3.7 | VLOAD wegnehmen, nur CN1 bleibt | ESP läuft ungestört weiter (Netze getrennt) | ☐ | |

## 4. Firmware aufspielen und Booten

Arduino IDE: Board „ESP32C3 Dev Module“ bzw. „ESP32S3 Dev Module“, USB CDC On Boot: Enabled, Partition Scheme „Default 4MB with spiffs“. Alternativ die fertige .bin aus GitHub Actions.

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 4.1 | Nur USB stecken, Sketch firmware/RC_Multiswitch hochladen | Upload ohne Fehler | ☐ | |
| 4.2 | Seriellen Monitor 115200 Baud öffnen, Reset drücken | Zeilen „CRSF gestartet (Board C3/S3 …)“, „RC-Multiswitch C3 v4.07“ bzw. S3, „SSID: MultiSwitch“, „IP: 192.168.1.1“ | ☐ | |
| 4.3 | USB ab, Modul nur über CN1 versorgen | WLAN „MultiSwitch“ erscheint nach wenigen Sekunden („Dauerhaft an“ ist ab Werk EIN) | ☐ | |
| 4.4 | nur S3: Status-LED ohne Empfänger | aus (kein Signal) | ☐ | |
| 4.5 | BOOT-Taster kurz drücken im Betrieb | nichts passiert, kein Neustart | ☐ | |
| 4.6 | BOOT beim Einstecken gedrückt halten | Modul startet im Download-Modus (kein WLAN), nach Reset ohne Taster wieder normal | ☐ | |

Wichtig: Ab Werk steht das RC-System auf CRSF (seit v4.07). Ein Modul mit älteren gespeicherten Einstellungen behält sein bisheriges RC-System.

### 4a. Nur C3: Strapping-Pin IO2 (Ausgang 3)

IO2 muss beim Einschalten HIGH sein. LED3/R3 und der ULN-Eingang ziehen ihn nach LOW, dann startet der C3 evtl. nicht. Die Platine bleibt so (Entscheidung 21.10.). Erkennen kannst du einen erfolgreichen Start am WLAN „MultiSwitch“.

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 4a.1 | 10-mal aus- und einschalten über CN1, ohne Last an Ausgang 3 | 10 von 10 Starts mit WLAN | ☐ | __ von 10 |
| 4a.2 | wie 4a.1, mit Verbraucher an Ausgang 3 und VLOAD an | 10 von 10 Starts | ☐ | __ von 10 |
| 4a.3 | wie 4a.1, aber über USB versorgt | 10 von 10 Starts | ☐ | __ von 10 |
| 4a.4 | Spannung an IO2 direkt nach dem Einschalten messen (vor dem ersten Schalten) | über ca. 2 V | ☐ | ___ V |

Startet er nicht sicher: R3 hochohmiger (z. B. 10 kΩ) oder LED3/R3 weglassen; als letzte Möglichkeit 10-kΩ-Pull-up von IO2 nach 3V3 nachrüsten. Danach 4a.1 bis 4a.3 wiederholen.

## 5. WLAN und Web-UI

Zugang ab Werk: WLAN „MultiSwitch“, Passwort 123456789, Adresse http://192.168.1.1

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 5.1 | Mit dem Handy ins WLAN, Browser 192.168.1.1 | Web-UI lädt, Reiter Übersicht, Ausgänge, RC-System, WiFi, Debug | ☐ | |
| 5.2 | Übersicht ansehen | Board C3 bzw. S3 und Version 4.07 angezeigt | ☐ | |
| 5.3 | Reiter RC-System: prüfen, dass „CRSF (ELRS/TBS)“ gewählt ist (sonst wählen, speichern, neu starten) | nach dem Neustart steht CRSF; serieller Monitor zeigt „CRSF gestartet … Geraeteadresse 0xC0 Slot 0“ | ☐ | |
| 5.4 | Reiter Ausgänge: eine Einstellung ändern, speichern, Strom aus und wieder an | Änderung ist noch da (NVS) | ☐ | |
| 5.5 | BOOT-Taster 3 s halten | WLAN geht aus (Handy verliert Verbindung) | ☐ | |
| 5.6 | BOOT-Taster nochmal 3 s halten | WLAN „MultiSwitch“ ist wieder da | ☐ | |
| 5.7 | Reiter WiFi: SSID ändern (z. B. MultiSwitch-Test), speichern, neu starten | neues WLAN erscheint; danach zurück auf „MultiSwitch“ | ☐ | |

## 6. Empfang vom Empfänger (CRSF, optional SBUS)

Empfänger an CN1: TX des Empfängers an Pin 3 (RX), RX des Empfängers an Pin 4 (TX), dazu +5 V und GND. Empfänger-Ausgang auf CRSF, 420000 Baud. RC-System steht auf CRSF (Schritt 5.3).

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 6.1 | Sender ein, Empfänger verbunden | Debug-Reiter: CRSF-Zähler steigen, kein CRC-Fehler-Anstieg | ☐ | |
| 6.2 | nur S3: Status-LED | grün, blinkt 500 ms an / 500 ms aus | ☐ | |
| 6.3 | Sender: ExpressLRS-Lua bzw. Geräte-Menü öffnen | Gerät „MultiSwitch@0“ erscheint | ☐ | |
| 6.4 | Einen Ausgang einschalten (Schritt 7), dann Sender ausschalten | Ausgang geht spätestens nach ca. 2 s aus (Failsafe) | ☐ | ___ s |
| 6.5 | nur S3: Status-LED bei Sender aus | schnell blinken (100 ms) oder aus, je nachdem ob der Empfänger noch Frames schickt | ☐ | |
| 6.6 | Sender wieder ein | Link kommt zurück, Ausgänge folgen wieder den Schaltern | ☐ | |
| 6.7 | WLAN-Auto-Failsafe: in Lua Ordner WLAN „Dauerhaft an“ = Aus, neu starten mit Sender an | kein WLAN | ☐ | |
| 6.8 | Sender ausschalten und warten (Auto Timeout ab Werk 60 s) | WLAN „MultiSwitch“ erscheint nach ca. 60 s | ☐ | ___ s |
| 6.9 | Optional SBUS: RC-System auf passendes SBUS (z. B. FrSky), Neustart, SBUS-Empfänger an CN1 Pin 3 | Ausgänge folgen dem eingestellten SBUS-Kanal | ☐ | |
| 6.10 | Optional SBUS: Empfänger abziehen | Ausgänge gehen nach ca. 10 s aus | ☐ | |

Nach 6.8 „Dauerhaft an“ wieder auf Ein stellen, wenn du es so haben willst. Nach 6.9/6.10 das RC-System wieder auf CRSF stellen.

## 7. Alle 8 Ausgänge

VLOAD an CN2 (z. B. 12 V), an jedem Ausgang von J1 ein Testverbraucher. Einschalten am einfachsten im Lua-Menü: Ordner „Ausgang N“, Feld „Test“ = Ein (wirkt bei Werkseinstellung Einzelkanal, Bit N). Danach mit dem Multiswitch-Widget am Sender (Adresse 0) gegenprüfen.

| Ausgang | GPIO C3 | GPIO S3 | LED leuchtet | Last an | Last aus bei Test = Aus | Notiz |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | IO0 | IO11 | ☐ | ☐ | ☐ | |
| 2 | IO1 | IO4 | ☐ | ☐ | ☐ | |
| 3 | IO2 | IO5 | ☐ | ☐ | ☐ | |
| 4 | IO3 | IO6 | ☐ | ☐ | ☐ | |
| 5 | IO4 | IO10 | ☐ | ☐ | ☐ | |
| 6 | IO5 | IO9 | ☐ | ☐ | ☐ | |
| 7 | IO6 | IO8 | ☐ | ☐ | ☐ | |
| 8 | IO7 | IO7 | ☐ | ☐ | ☐ | |

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 7.1 | Nur ein Ausgang an: schalten nur LED und Last dieses Ausgangs? | keine Nachbarn gehen mit an | ☐ | |
| 7.2 | Alle 8 Ausgänge über das Widget am Sender schalten | jeder Schalter trifft den richtigen Ausgang | ☐ | |
| 7.3 | Ausgang 1 auf Blinken, AN 50, AUS 50 (*10 ms) | blinkt 0,5 s an / 0,5 s aus | ☐ | |
| 7.4 | Ausgang 1: PWM Festwert 64 | Last deutlich dunkler als bei 255 | ☐ | |
| 7.5 | nur C3: Ausgang 7 und 8 mit PWM Festwert 64 und 200 | 64 = aus, 200 = voll an (nur digital, an ab 50 %) | ☐ | |
| 7.6 | nur S3: Ausgang 7 und 8 mit PWM Festwert 64 | gedimmt wie die anderen | ☐ | |
| 7.7 | Ein Ausgang mit ca. 300-500 mA Last, 5 min an | ULN2803A handwarm, nicht heiß; Spannung am Ausgang unter ca. 1,2 V | ☐ | ___ mA / ___ V |
| 7.8 | Strom an CN2 mit allen 8 Ausgängen an messen | unter ca. 2 A (Grenze JST-PH-Kontakt) | ☐ | ___ A |

## 8. Lua-Menü am Sender

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 8.1 | „MultiSwitch@0“ öffnen | Version, Ordner Global, Ausgang 1-8, WLAN, UART B/C | ☐ | |
| 8.2 | Feld Version ablesen | „v4.07 C3“ bzw. „v4.07 S3“ | ☐ | |
| 8.3 | Ausgang 2: Blink auf Blinken stellen, Web-UI neu laden | Web-UI zeigt dieselbe Einstellung | ☐ | |
| 8.4 | Strom aus und an, Lua erneut öffnen | Einstellung aus 8.3 ist noch da | ☐ | |
| 8.5 | Global „Switch Addr“ auf 1, Geräteliste neu laden | Gerät heißt „MultiSwitch@1“; Widget mit Adresse 1 schaltet, mit Adresse 0 nicht mehr | ☐ | |
| 8.6 | Adresse zurück auf 0 | wieder „MultiSwitch@0“ | ☐ | |
| 8.7 | nur C3: Ordner UART B/C | UART C und UART C Baud zeigen „nicht vorhanden (C3)“ | ☐ | |
| 8.8 | Lua bleibt bedienbar, während die Ausgänge geschaltet werden | kein Hängen, keine Abbrüche | ☐ | |

## 9. UART-Ports B und C (CRSF, S.Port, GPS)

UART B (J5) gibt es bei C3 und S3, UART C (J6) nur beim S3. Rolle und Baudrate stellst du im Lua-Ordner „UART B/C“ oder in der Web-UI (Reiter RC-System) ein. Eine neue Rolle wirkt erst nach einem Neustart. Ab Werk stehen beide auf CRSF.

### 9a. S.Port (LiPo-Sensor)

FLVSS/MLVSS: TX des Ports über Diode 1N4148 und RX zusammen an die Signalleitung des Sensors.

| Nr | Prüfung | Erwartet | OK B | OK C (S3) | Notiz |
| --- | --- | --- | --- | --- | --- |
| 9a.1 | Rolle S.Port, Neustart, Sensor an Akku | Debug-Reiter zeigt Zellspannungen (Abweichung zum Multimeter unter 0,05 V) | ☐ | ☐ | |
| 9a.2 | Am Sender „Sensoren suchen“ | Zellspannungen kommen als Telemetrie an (alle 100 ms) | ☐ | ☐ | |
| 9a.3 | Optional zweiter Sensor (Poll-ID 0x22) | beide Akkus werden angezeigt | ☐ | ☐ | |

### 9b. GPS

| Nr | Prüfung | Erwartet | OK B | OK C (S3) | Notiz |
| --- | --- | --- | --- | --- | --- |
| 9b.1 | Rolle GPS, Baudrate Auto, Neustart, GPS im Freien | Auto findet die Baudrate und stellt das GPS auf 115200 Baud / 10 Hz um | ☐ | ☐ | |
| 9b.2 | Warten auf Fix | Debug-Reiter zeigt Satelliten, Position, Geschwindigkeit | ☐ | ☐ | |
| 9b.3 | Am Sender „Sensoren suchen“ | GPS-Werte als Telemetrie | ☐ | ☐ | |
| 9b.4 | GPS aus- und wieder einstecken | wird ohne Neustart des Moduls wieder gefunden | ☐ | ☐ | |
| 9b.5 | nur S3: UART B und C beide auf GPS | nur UART B arbeitet, UART C bleibt aus | ☐ | | |

### 9c. CRSF-Modulkette (2 und 3 Module)

Modul 1 hängt am Empfänger, Modul 2 per 1:1-Kabel an J5 von Modul 1, Modul 3 an J5 von Modul 2 (oder beim S3 an J6 von Modul 1). Jedes Modul bekommt vorher eine eigene Adresse (0, 1, 2).

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 9c.1 | 2 Module, Geräteliste am Sender | „MultiSwitch@0“ und „MultiSwitch@1“ | ☐ | |
| 9c.2 | Einstellung bei @1 ändern | nur Modul 2 ändert sich, Modul 1 bleibt gleich | ☐ | |
| 9c.3 | Widget Adresse 0 und 1 schalten | jeweils nur das richtige Modul schaltet | ☐ | |
| 9c.4 | 3 Module, Geräteliste | alle drei erscheinen, auch nach mehrmaligem Neuladen | ☐ | |
| 9c.5 | Sender aus | alle Module gehen nach ca. 2 s in Failsafe | ☐ | |
| 9c.6 | nur S3: Modul an J5 und eins an J6 gleichzeitig | beide erreichbar, keine doppelten Einträge, keine Endlosschleife (Debug: Router-Zähler steigen gleichmäßig) | ☐ | |
| 9c.7 | Zwei Module absichtlich mit gleicher Adresse | Warnung im Debug-Reiter, S3-LED Doppelblitz | ☐ | |
| 9c.8 | Debug-Reiter von Modul 1 | Zähler „verworfen“ steigt kaum; keine CRC-Fehler beim Nachbarn | ☐ | |
| 9c.9 | Optional Latenz: Ausgang 1 an Modul 1 und 3 gleichzeitig schalten, Oszilloskop oder Logikanalysator | Versatz je Modul wenige ms | ☐ | ___ ms |

Die Rolle Raw ist für Sonderfälle und wird hier nicht geprüft.

## 10. Sichern, Export/Import und OTA

Alles in der Web-UI, Karte „Konfiguration sichern/wiederherstellen“. Das Modul dabei über CN1 versorgen, nicht nur über USB.

| Nr | Prüfung | Erwartet | OK | Notiz |
| --- | --- | --- | --- | --- |
| 10.1 | „Im Modul sichern“ | Meldung „Im Modul gesichert“ | ☐ | |
| 10.2 | „Aus Modul laden“ | Liste zeigt das Backup mit Datum/Name | ☐ | |
| 10.3 | Eine Einstellung ändern, dann das Backup aus 10.1 laden | alte Einstellung ist wieder da | ☐ | |
| 10.4 | Ein Backup in der Liste löschen | Sicherheitsabfrage, danach ist es weg | ☐ | |
| 10.5 | JSON-Export auf Handy/PC speichern | Datei wird heruntergeladen | ☐ | |
| 10.6 | Werkseinstellungen „Zurücksetzen“, dann JSON-Import | vorher wird automatisch im Modul gesichert; danach alle Einstellungen wie vor dem Reset | ☐ | |
| 10.7 | Firmware-Update (OTA) mit der .bin aus GitHub Actions | Upload läuft durch, Modul startet neu, Version stimmt, Einstellungen bleiben | ☐ | |
| 10.8 | Nach dem OTA „Aus Modul laden“ | automatisches Backup von vor dem Update ist in der Liste | ☐ | |
| 10.9 | Optional: alte V3-JSON-Konfiguration importieren | wird angenommen, Ausgänge wie in V3 | ☐ | |

## 11. Ergebnis

| Schritt | Bestanden | Bemerkung |
| --- | --- | --- |
| 2 Sichtprüfung | ☐ ja ☐ nein | |
| 3 Versorgung | ☐ ja ☐ nein | |
| 4 Booten (C3 mit 4a) | ☐ ja ☐ nein | |
| 5 WLAN und Web-UI | ☐ ja ☐ nein | |
| 6 Empfang | ☐ ja ☐ nein | |
| 7 Ausgänge | ☐ ja ☐ nein | |
| 8 Lua | ☐ ja ☐ nein | |
| 9 UART B/C | ☐ ja ☐ nein | |
| 10 Sichern und OTA | ☐ ja ☐ nein | |

Gesamt: ☐ abgenommen ☐ abgenommen mit Einschränkungen ☐ nicht abgenommen

Datum, Unterschrift: ______________________

### Hinweise aus dem Quellcode

- Lua „Switch Addr“ lässt 0-20 zu, die Firmware nutzt aber nur 0-15. Werte 16-20 verhalten sich wie 15.
- Die Pin-Prüfungen in 2.7 bis 2.9 setzen voraus, dass die Belegung aus den READMEs zum gebauten PCB passt. Beim S3 steht der DRC laut README noch aus.
