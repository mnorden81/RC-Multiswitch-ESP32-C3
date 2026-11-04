# RC-Multiswitch-ESP32-C3

RC-Multiswitch mit 8 Schaltkanaelen auf einem ESP32-C3 SuperMini.

Frueher `CRSF-Multiswitch-ESP32-C3`. Der neue Name ist neutral, weil der Multiswitch neben CRSF auch SBUS (UART A) als Eingang versteht.

Kleiner, guenstiger Multiswitch fuer RC-Modelle: Der ESP32-C3 empfaengt CRSF vom Empfaenger und schaltet ueber einen TBD62083APG (Nachfolger des ULN2803A) bis zu 8 Verbraucher (Licht, Relais, Funktionen). Das Layout folgt dem CRSF Multiswitch THT v1.1, alle Bauteile ausser den JST-GH-Buchsen sind bedrahtet.

Dokumente:
- [docs/Projektbeschreibung.docx](docs/Projektbeschreibung.docx): Projektbeschreibung
- [docs/Hardware-Beschreibung_C3_S3.docx](docs/Hardware-Beschreibung_C3_S3.docx): Hardware-Beschreibung C3 und S3 (Stecker, Kanalzuordnung, Stueckliste, Dimensionierung)
- [docs/Abnahmepruefung.md](docs/Abnahmepruefung.md): Abnahmepruefung (Pruefliste fuer ein fertig gebautes Modul)
- [docs/Firmware-Spezifikation.md](docs/Firmware-Spezifikation.md) (auch als DOCX): Firmware-Spezifikation (Basis V3, Router fuer Modulketten, BOOT-Taster, Status-LED)

## Merkmale
- 8 Schaltkanaele ueber TBD62083APG (negativ) oder TBD62783APG (positiv), Kontroll-LED je Kanal
- UART A (Eingang vom Empfaenger) und UART B (Rolle waehlbar: Modulkette CRSF, S.Port-LiPo-Sensoren oder GPS)
- Versorgung des ESP32 aus +5 V des Empfaengers, Last getrennt mit 5-12 V
- Eigener THT-Footprint fuer den SuperMini im Projekt

## Hardware (v0.3 (Entwurf))
Board: ESP32-C3 SuperMini

- Lastspannung 5-12 V (VLOAD) an CN2 (JST PH 2), TVS-Diode P6KE18A als Schutz.
- Treiber TBD62083APG (DMOS, Nachfolger des ULN2803A, gleiche Pinbelegung; ein ULN2803A passt weiterhin in den Sockel), 8 Kanaele, max. 500 mA je Kanal, Summe aller Kanaele ca. 1,5 A. Spannungsabfall am Ausgang nur ca. 0,2-0,4 V statt ca. 1 V beim ULN2803A. Positiv schaltende Variante mit TBD62783APG siehe [hardware/README-hardware.md](hardware/README-hardware.md).
- R9-R16 (THT 1/4 W) zwischen Treiber-Ausgang und Stiftleiste J1: kein Wert vorgegeben, der Anwender legt sie passend zu Verbraucher und Lastspannung aus.
- R1-R8 und LED1-LED8 (3 mm) als Kontroll-LED je Kanal, vom Steuersignal Sn gegen GND. Werte legt der Anwender fest, eine Empfehlung ist auf der Platine aufgedruckt.
- Keine Pulldowns und keine Widerstaende in den UART-Leitungen. Der ESP32 wird aus +5 V von CN1 (BEC/Empfaenger) versorgt.

### Belegung
| Funktion | GPIO |
|---|---|
| S0..S7 | IO0..IO7 |
| UART A (CN1, Eingang) | RX IO20, TX IO21 |
| UART B (J5) | TX IO10, RX IO8 |

### Anschluesse
- CN1 UART A (JST-GH 4): 1 GND, 2 +5 V, 3 RX, 4 TX
- J5 UART B (JST-GH 4): 1 GND, 2 +5 V, 3 TX, 4 RX (1:1-Kabel zum naechsten Modul)
- CN2 Last 5-12 V (JST PH 2, max. ca. 2 A je Kontakt)
- J1 Ausgaenge S0..S7

### Hinweise
- IO8 haengt beim SuperMini an der Onboard-LED, IO9 am BOOT-Taster. UART B RX liegt auf IO8.
- **Risiko IO2 (Ausgang 3):** IO2 ist ein Strapping-Pin und muss beim Einschalten HIGH sein. LED3/R3 und der Treiber-Eingang koennen ihn nach LOW ziehen, der C3 startet dann evtl. nicht sicher. Die Platine bleibt so (bereits bestellt). Beim ersten Aufbau mehrmals ein- und ausschalten; Abhilfe siehe [firmware/README.md](firmware/README.md#bekanntes-risiko-c3-io2-ausgang-3-ist-ein-strapping-pin).
- Footprint ESP32-C3-SuperMini_THT ist eine eigene Zeichnung (2x8, 2,54 mm, Reihenabstand 15,24 mm). Vor der Fertigung 1:1 am echten Board pruefen.

## Firmware (v4.07)
- Arduino-Sketch `firmware/RC_Multiswitch`, gleicher Quellcode fuer C3 und S3 (Board wird automatisch erkannt). Basis: MultiSwitch_ESP32_V3 v3.12.
- CRSF auf UART A (Werkseinstellung ab v4.07), wahlweise SBUS. UART B (und UART C beim S3) per Lua oder Web-UI auf Aus, CRSF (Modulkette), S.Port, GPS oder Raw einstellbar, mit eigener Baudrate je UART. Beim GPS sucht die Baudrate „Auto“ (Vorgabe) die Rate selbst und stellt das GPS auf 115200 Baud und 10 Hz um, wie bei Betaflight. In der Modulkette ist jedes Modul mit eigener Adresse ueber Lua einzeln einstellbar.
- Gemeinsame Basis aller ESP32-Module seit v4.05: `firmware/RC_Multiswitch/src/RC_Common/` (CRSF-Bibliothek mit Router, UART-Rollen, Lua-Menue, NVS, WLAN-Failsafe, Status-LED, OTA), siehe deren README.
- BOOT-Taster 3 s: WLAN-AP ein/aus. Status-LED nur beim S3.
- Details und Bauanleitung: [firmware/README.md](firmware/README.md).

## Ordner
- `hardware/`: KiCad-Projekt (Schaltplan, PCB, PDF, eigene Footprints, fp-lib-table). Entwurfsnotizen in [hardware/README-hardware.md](hardware/README-hardware.md). 3D-druckbares Gehaeuse (stehende oder gewinkelte Stiftleiste) in [hardware/gehaeuse/](hardware/gehaeuse/README.md).
- `firmware/`: Firmware v4.07 (Arduino-Sketch).
- `docs/`: Projektbeschreibung, Hardware-Beschreibung und Firmware-Spezifikation.

## Stand
- Hardware: Schaltplan und PCB vorhanden. ERC/DRC noch in KiCad ausfuehren.
- Firmware: v4.07 kompiliert fuer C3 und S3, noch nicht auf Hardware getestet.

## Offene Punkte
- Pad-Namen und Footprint am realen Board pruefen
- Erwaermung des Treibers bei mehreren Kanaelen mit 500 mA pruefen
- Firmware auf Hardware testen (Einzelmodul und Kette mit 2-3 Modulen)
- IO2-Strapping (Ausgang 3) beim ersten Aufbau pruefen
