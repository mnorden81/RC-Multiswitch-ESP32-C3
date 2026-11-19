# Firmware RC-Multiswitch

Arduino-Sketch in `RC_Multiswitch/`, gleicher Quellcode fuer C3, S3 und ab v5.00 den klassischen ESP32 (Platinen Basis D1 Mini und TXRX, Auswahl zur Laufzeit in der Web-UI-Karte „Platine“ oder Lua Global > „Platine (Neustart)“). Basis ist MultiSwitch_ESP32_V3 v3.12. Spezifikation: `docs/Firmware-Spezifikation.md`.

## Bauen mit der Arduino IDE
- Board-Paket: esp32 von Espressif, Version 3.x (getestet im CI mit 3.0.7)
- Bibliotheken: Bolder Flight Systems SBUS 8.1.4, TinyGPSPlus 1.0.3 (ab v4.04). Alles andere liegt im Sketch unter `src/RC_Common/` (ab v4.05, gemeinsame Basis aller ESP32-Module, siehe `src/RC_Common/README.md`)
- Board: **ESP32C3 Dev Module** (C3 SuperMini), **ESP32S3 Dev Module** (S3-Zero) oder **ESP32 Dev Module** (Basis/TXRX). Das Board wird in `board_config.h` automatisch erkannt.
- **USB CDC On Boot: Enabled** (sonst bricht der Build mit einer Meldung ab, UART0 wird fuer CRSF/SBUS gebraucht)
- Partition Scheme: eines mit OTA, z.B. "Default 4MB with spiffs"
- Fertige .bin-Dateien fuer C3 und S3 erzeugt GitHub Actions bei jedem Push (Artefakte im Workflow "firmware").

## Funktionen
- Alle Funktionen der V3 (Konfig 1/2/3 je Ausgang, MKan1/MKan2, Web-UI, Lua, Failsafe, NVS, OTA, JSON-Export/-Import).
- UART A (CN1): CRSF (RC-System 4, Werkseinstellung ab v4.07) oder SBUS (RC-System 0-3) vom Empfaenger.
- C3: Ausgang 7/8 nur digital (an ab 50 %), Ausgang 1-6 PWM. S3: alle 8 PWM.
- **UART B/C mit waehlbarer Rolle (ab v4.04):** UART B (C3 und S3) und UART C (nur S3) koennen im Lua-Menue (Ordner "UART B/C") oder in der Web-UI (RC-Tab) auf Aus, CRSF, S.Port, GPS oder Raw (ab v4.05) gestellt werden, wie beim Soundmodul. Ab v4.05 hat jeder UART eine eigene Baudrate (Lua-Felder 84/85, vorher 84 = GPS-Baudrate); beim Wechsel der Rolle wird die passende Baudrate gesetzt. Wirkt nach einem Neustart. Werkseinstellung: CRSF auf beiden.
  - CRSF: Modulkette zum naechsten Modul (siehe unten), nur bei RC-System CRSF.
  - S.Port: bis zu 2 FrSky FLVSS/MLVSS LiPo-Sensoren (Poll-ID 0xA1 und 0x22), Anschluss TX ueber Diode 1N4148 und RX zusammen an die Signalleitung (siehe `sport_lipo.h`).
  - GPS: NMEA-Empfaenger (z. B. ATGM336H), Baudrate 9600-115200 waehlbar.
  - Bei CRSF gehen Zellspannungen und GPS alle 100 ms als Telemetrie an den Sender. Bei SBUS werden die Werte nur im Debug-Tab angezeigt.
  - S.Port und GPS gibt es nur einmal: steht UART C auf derselben Rolle wie UART B, bleibt UART C aus.
- **Modulkette (nur CRSF):** UART B (C3 und S3) und UART C (nur S3) mit Rolle CRSF gehen zum naechsten Modul. Jedes Modul braucht eine eigene Modul-Adresse (0-15). Alle Module erscheinen im Lua-Menue als `<Name>@<Adresse>` und lassen sich einzeln einstellen.
- **BOOT-Taster:** 2 s gedrueckt halten (bis v4.09: 3 s) schaltet den WLAN-AP ein oder aus (bis zum Neustart, die Einstellung "Dauerhaft an" bleibt unveraendert).
- **Status-LED (nur S3), gleiches Schema wie alle Module (ab v4.10):** gruen langsam (500 ms) = OK, rot schnell (100 ms) = Failsafe bzw. kein RC-Link, rot Aufblitzen (kurz alle 1 s) = kein Signal, blau Doppelblitz = doppelte Modul-Adresse in der Kette, violett statt gruen/rot = WLAN an. Rot und Gruen vertauscht? Lua Global > "LED Farbfolge" auf GRB stellen (Vorgabe RGB fuer den S3-Zero).
- **Funk (ab v5.01, ESP-NOW):** Module ohne Kabel zum Empfaenger. RC-System 5 „CRSF + Funk senden (Zentrale)“ am Modul am Empfaenger, RC-System 6 „CRSF aus Funk (Teilnehmer)“ an den anderen Modulen (UART A bleibt dort frei). Kanaele, Lua und Telemetrie laufen ueber Funk, die Zentrale ist Router-Port D. Einstellungen in der Web-UI (Karte „Funk“ im RC-Tab) oder im Lua-Ordner „Funk“ (88-95): Fahrzeug-Kennung und Funkkanal ueberall gleich, Sendeleistung, Kanal-Rate (Zentrale), Rueckkanal (Teilnehmer). Wirkt nach Neustart. WLAN laeuft dann auf dem Funkkanal. Reiter „Funk“: Ampel, Gegenstellen, Verlust, RSSI. Failsafe nach 2 s ohne Funk-Daten. Gelber Doppelblitz = zweite Zentrale mit derselben Kennung. Code: `src/RC_Common/funk_link.*`.
- Debug-Tab der Web-UI: CRSF-Zaehler plus Router-Zaehler (weitergeleitet, verworfen) und Warnung bei doppelter Adresse.

## Router-Regeln
- A -> B/C: alle gueltigen Frames, ausser Extended-Frames an die eigene Adresse.
- B/C -> A: alle gueltigen Frames.
- B <-> C: nie.
- Funk (Port D, nur Zentrale) wie B/C: Frames von A gehen in den Funk, Antworten aus dem Funk nach A.
- Frames gehen ganz und unveraendert weiter (CRC geprueft). Je Port eine Warteschlange mit 8 Frames; bei Ueberlauf werden zuerst alte RC-Kanal-Frames verworfen.

## Stand
- Aktuelle Version und alle Änderungen: [CHANGELOG.md](../CHANGELOG.md).
- v5.04 kompiliert für C3, S3 und ESP32 (CI). Funk-Teilnehmer (S3) auf Hardware: Kanäle, WM und Lua laufen.
- Offen: Abnahmetest nach [docs/Abnahmepruefung.md](../docs/Abnahmepruefung.md) (Einzelmodul, Kette mit 2 und 3 Modulen).

## Bekanntes Risiko C3: IO2 (Ausgang 3) ist ein Strapping-Pin
IO2 muss beim Einschalten HIGH sein, damit der ESP32-C3 normal startet. Auf der Platine haengen an IO2 (Ausgang 3) die Kontroll-LED LED3 mit R3 nach GND und der Eingang des Treibers (TBD62083APG bzw. ULN2803A). Beides kann IO2 beim Reset nach LOW ziehen, der C3 startet dann evtl. nicht oder nur unzuverlaessig. Die Platine bleibt bewusst so (bereits bestellt, Stand 21.10.2026).
- Beim ersten Aufbau pruefen: mehrmals aus- und einschalten, mit und ohne Last an Ausgang 3.
- Startet der C3 nicht sicher: R3 hochohmiger waehlen (z. B. 10 kOhm) oder LED3/R3 weglassen; als letzte Moeglichkeit einen 10-kOhm-Pull-up von IO2 nach 3V3 nachruesten.
- Der S3 ist nicht betroffen.
