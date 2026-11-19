# Versionsgeschichte RC-Multiswitch (C3, S3, ESP32 Basis/TXRX)

Gleiche Firmware für alle Platinen, deshalb gleiche Versionsnummern in den Repos RC-Multiswitch-ESP32-C3, RC-Multiswitch-ESP32-S3 und (ab v5.00) ESP32-Multiswitch-Basis_Ziege-One. Die Version wird bei jeder Änderung erhöht, weil sie als CRSF „Parameter Version Number“ an den Sender geht. Neueste Version oben.

## v5.01 (RC_Common 1.5.0)
- Neu: **Funk** (ESP-NOW, aus der Funk-Brücke v0.1.9). Module ohne Kabel zum Empfänger bekommen CRSF per Funk. RC-System 5 = „CRSF + Funk senden (Zentrale)“: das Modul am Empfänger funkt alles vom Kabel weiter. RC-System 6 = „CRSF aus Funk (Teilnehmer)“: Kanäle, Lua und Telemetrie laufen über Funk, UART A bleibt frei. Pro Fahrzeug eine Zentrale und bis zu 8 Teilnehmer, eine Funk-Brücke kann an jeder Seite stehen. Noch nicht auf Hardware getestet.
- Einstellungen: Fahrzeug-Kennung (1–255), Funkkanal (1–13), Sendeleistung (2–20 dBm, Vorgabe 20), bei der Zentrale „Kanäle alle“ (Vorgabe 10 ms), beim Teilnehmer „Rückkanal“ (Lua/Telemetrie, Vorgabe an). Web-UI Reiter RC-System, Karte „Funk“, oder Lua-Ordner „Funk“ (Felder 88–95). Wirken nach Neustart. NVS `fkid fkch fkpwr fkrate fkback`.
- Web-UI: neuer Reiter „Funk“ mit Ampel, Gegenstellen (Rolle, CRSF-Adresse, Pakete/s, Verlust, RSSI, Aussetzer) und Zählern, Zeile in der Übersicht. `/api/funk`, `/api/funk/reset`.
- Failsafe wie bei abgezogenem Kabel: ohne Funk-Daten nach 2 s alle Ausgänge aus.
- Zweite Zentrale mit derselben Kennung: gelber Doppelblitz. Gegenstelle mit derselben CRSF-Adresse: blauer Doppelblitz.
- Mit Funk läuft das WLAN auf dem Funkkanal (ein Funkteil für beides).

## v5.00
- Eine Firmware für alle vier Platinen: C3, S3 und neu der klassische ESP32 mit den Platinen **Basis** (ESP32 D1 Mini) und **TXRX** aus ESP32-Multiswitch-Basis_Ziege-One. Ersetzt dort MultiSwitch_ESP32_V3 und MultiSwitch_ESP32_TXRX (v3.17); V2 bleibt unverändert.
- Der Chip wird beim Kompilieren erkannt (Board „ESP32 Dev Module“ für Basis/TXRX). Basis oder TXRX wählt man zur Laufzeit: Web-UI Reiter RC-System, Karte „Platine“, oder Lua Global > „Platine (Neustart)“ (Feld 87, NVS `board`, Vorgabe Basis). Die Ausgangspins wechseln nach einem Neustart. Werkseinstellungen lassen die Platine unverändert.
- Basis/TXRX wie bis v3.17: CRSF/SBUS auf GPIO16/17 (UART2), Status-LED GPIO2, GPIO13 beim Start auf GND = WLAN an. Kein BOOT-Taster (der D1 Mini hat nur Reset), WLAN wie bisher über GPIO13, Web-UI oder Lua. Neu dazu: Lua-Menü mit Ordneransicht, Einstellungs-Backup im Flash. UART B/C sind auf diesen Platinen nicht herausgeführt und werden ausgeblendet.
- Version in Web-UI und Lua mit Platine, z. B. „v5.00 TXRX“. Karte „Platine“ zeigt Pins, LED und WLAN-Start der aktiven Platine.
- Gespeicherte Einstellungen aus v3.17 bleiben erhalten (gleicher NVS-Bereich `msw`). CI baut zusätzlich das ESP32-Image.

## v4.11
- Baut mit esp32-Core 3.3.x (Arduino IDE): `BOOT_PIN` heißt jetzt `BOOT_BTN_PIN`, weil der neue Core `BOOT_PIN` selbst definiert. CI baut zusätzlich mit 3.3.12.

## v4.10 (RC_Common 1.4.0)
- Status-LED (S3) mit demselben Farbschema wie alle Module: grün langsam = OK, rot schnell = Failsafe / kein RC-Link, rot Aufblitzen = kein Signal (vorher aus), blau Doppelblitz = doppelte Moduladresse, violett statt grün/rot = WLAN an.
- Neu: Lua Global > „LED Farbfolge“ (Feld 86, NVS `ledrgb`), RGB (S3-Zero, Vorgabe) oder GRB. Beim C3 ausgeblendet.
- BOOT-Taster 2 s halten (vorher 3 s) schaltet das WLAN.

## v4.09 (RC_Common 1.3.0)
- Fix: lange Lua-Auswahlfelder (Ausgang-Quelle, UART-Baudrate) kommen Chunk für Chunk, das ELRS-Lua zeigt sie jetzt vollständig.
- Ordnernamen zeigen den aktuellen Wert, z. B. „Ausgang 1 (Kanal_L 5)“.
- Felder ohne Wirkung werden ausgeblendet (Feld-IDs bleiben).

## v4.08
- Lua: „PWM Festwert“ bleibt bei MWprop ein gesperrtes Zahlenfeld statt Info-Feld (sonst erst nach Verlassen des Menüs einstellbar).

## v4.07
- Werkseinstellung RC-System jetzt 4 = CRSF (vorher FrSky SBUS). Gespeicherte Einstellungen bleiben.
- Fix: Lua-Feld „Version“ zeigte fest „v4.05“.

## v4.06 (RC_Common 1.2.0)
- Neu: Einstellungs-Backup im Flash (Tab WLAN, „Konfiguration sichern“), die letzten 5 Backups bleiben.
- Automatisches Backup vor jedem Import und Firmware-Update (die letzten 3 bleiben).
- Braucht ein Partitionsschema mit SPIFFS („Default 4MB with spiffs“).

## v4.05 (RC_Common 1.1.0)
- Gemeinsamer Code aller ESP32-Module in `src/RC_Common/` (CRSF-Bibliothek 1.1.0 mit Router, UART-Rollen, S.Port, GPS, Lua-Menü als Tabelle, NVS, WLAN-Failsafe, Status-LED, OTA). Eigene Kopien `crsf_esp32.*`, `sport_lipo.*`, `gps_speed.*` entfallen.
- Fix: Command-CRC (0xBA) laut Spezifikation.
- UART B/C: neue Rolle „Raw“ und Baudrate je UART (Lua-Felder 84/85, Feld 84 war „GPS Baud“). Rollennummern 0 Aus, 1 CRSF, 2 S.Port, 3 GPS, 4 Raw.
- Neu: Baudrate „Auto“ für GPS (sucht 9600–115200, stellt das GPS auf 115200 Baud / 10 Hz).
- NVS: gemeinsame Schlüssel (`wip`, `madr`, `wfauto`, `wftmo`, `wfalways`, `u1role`, `u1baud`, `u2role`, `u2baud`), alte Werte werden einmalig übernommen.

## v4.04
- Neu: Rolle von UART B (C3/S3) und UART C (S3) wählbar: Aus, CRSF (Modulkette), S.Port (FLVSS/MLVSS) oder GPS. Lua-Ordner „UART B/C“ und Web-UI.
- Bei CRSF gehen Zellspannungen und GPS alle 100 ms als Telemetrie an den Empfänger.
- Neue Bibliothek TinyGPSPlus, neue NVS-Schlüssel `pbrole`, `pcrole`, `gpsbaud`.

## v4.03
- Fix: SBUS-Zeitlimit. Kommen 10 s keine SBUS-Frames, gilt das Signal als weg und die Ausgänge gehen aus.

## v4.02
- Fix: CRSF-Link-Statistik (Frame 0x14) war um ein Byte verschoben, die LED zeigte bei Empfängern mit einer Antenne fälschlich „kein RC-Link“.

## v4.01
- Neu: BOOT-Taster lang drücken schaltet den WLAN-AP um.
- Neu: CRSF-Router für Modulketten über UART B/C (A → B/C alles außer Extended-Frames an die eigene Adresse, B/C → A alles, nie B ↔ C). Jedes Modul ist über Lua einzeln erreichbar („Name@Adresse“).
- Neu: doppelte Moduladresse wird erkannt (Doppelblitz, Warnung im Debug-Tab).
- Fix: CRSF-Parser verlor Frames, die über zwei Loop-Durchläufe verteilt ankamen.

## v4.00
- Neue Platinen ESP32-C3 SuperMini und ESP32-S3-Zero, `board_config.h` erkennt den Chip.
- CRSF und SBUS beide auf UART A (CN1), Debug über USB-CDC.
- WifiPin GPIO13 entfällt. C3: Ausgang 7/8 nur digital (6 LEDC-Kanäle).
- Status-LED: S3 WS2812, C3 ohne LED.

## Vorgeschichte (ESP32-MultiSwitch V3, Repo ESP32-Multiswitch-Basis_Ziege-One)

RC-Multiswitch v4.00 ist von ESP32-MultiSwitch V3 v3.12 abgezweigt. Die wichtigsten Schritte davor:

- **v3.12:** CRSF „Parameter Version Number“ im DEVICE_INFO enthält die Firmware-Version (vorher fest 0).
- **v3.10:** bis zu 3 Konfigurationen je Ausgang (Priorität 1 > 2 > 3), Konfig 2/3 nur in der Web-UI.
- **v3.00:** MKan-Gruppen: 2 zusätzliche 8-Bit-Kanalquellen (MKan1/MKan2, Ausgang_Kanal 80–95).
- **v2.00:** CRSF-Diagnosezähler, Konfiguration als JSON exportieren/importieren, WLAN-Auto-Failsafe, Firmware-Update per WLAN (OTA).
- **v0.14:** MWprop aus ESP32-RC-Sound übernommen, CRSF-Einkanal-Timeout 2000 ms.

Ausführliche Liste der V2/V3-Versionen: CHANGELOG.md im Repo ESP32-Multiswitch-Basis_Ziege-One.
