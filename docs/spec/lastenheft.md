---
title: "Lastenheft"
subtitle: "Miniaturisierter Beschleunigungs-Datenlogger für Tiere"
version: "0.1 (Entwurf)"
date: "17.10.2026"
author: "Laurenz Untiedt, [Name 2], [Name 3], [Name 4], [Name 5]"
lang: de-DE
toc-title: "Inhaltsverzeichnis"
course: "Capstone-Projekt (CAP) – Prof. Dr. Markus Cremer – WS 26/27 – TH Köln"
---

# Lastenheft – Miniaturisierter Beschleunigungs-Datenlogger für Tiere

Capstone-Projekt (CAP) · Prof. Dr. Markus Cremer · WS 26/27 · TH Köln\
Version 0.1 (Entwurf) · 17.10.2026\
Erstellt von: Laurenz Untiedt, [Name 2], [Name 3], [Name 4], [Name 5]

## A Änderungsprotokoll

| Version | Änderungen | Datum | Geändert von |
|---|---|---|---|
| 0.1 | Erstellung des initialen Lastenhefts auf Basis der Themenbeschreibung des ERTS Lab | 17.10.2026 | LU |

## 1 Einführung

Gesucht ist ein kleiner, batteriebetriebener Datenlogger, der die Beschleunigung von Tieren aufzeichnet und die Rohdaten anschließend drahtlos bereitstellt. Auftraggeber ist das **ERTS Lab** (Prof. Dr. Markus Cremer, TH Köln), Anwendungspartner der **Zoo Wuppertal**. Auftragnehmer ist ein Team aus fünf Studierenden im Capstone-Projekt des Wintersemesters 2026/27.

## 2 Ausgangssituation

In einem Vorgängerprojekt am ERTS Lab wurden Verfahren zur Aktivitätsklassifikation, zur Schrittzählung und zu den Aktivitätsmaßen ODBA/VeDBA entwickelt – auf einem Evaluationsboard (ST SensorTile.box PRO mit LSM6DSV16X). Dieses Board ist für den Einsatz an einem lebenden Tier zu groß und zu empfindlich. Alle weiteren Schritte des Forschungsstrangs benötigen jedoch echte Messdaten von Tieren.

Die Schwierigkeit liegt in einem Zielkonflikt: Abtastrate, Energiebedarf, Batteriegröße, Speicherkapazität und Aufzeichnungsdauer begrenzen sich gegenseitig. Bei 50 Hz, drei Achsen und 16 Bit fallen rund 26 MB pro Tag an – mehr, als ein typischer serieller NOR-Flash fasst.

## 3 Ziele und Nutzen

### 3.1 Ziele

- **Z1:** Ein am Tier tragbarer Prototyp zeichnet dreiachsige Beschleunigungsrohdaten auf.
- **Z2:** Die Zielwerte für Abtastrate, Aufzeichnungsdauer, Masse und Größe sind aus den Analyseanforderungen hergeleitet und begründet.
- **Z3:** Die Daten lassen sich drahtlos auslesen und direkt in die Analysekette des Labors übernehmen.
- **Z4:** Stromaufnahme, erreichbare Aufzeichnungsdauer und Signalqualität sind gemessen.
- **Z5:** Eine erste Praxisaufnahme belegt, dass die Daten für ODBA/VeDBA nutzbar sind.
- **Z6:** Alle Ergebnisse liegen zum Abgabetermin des Capstone-Projekts [Datum] vor.

### 3.2 Erwarteter Nutzen

- **Wissenschaftlich-technisch:** Echte Tierdaten ermöglichen die Validierung der Klassifikationsalgorithmen und stützen die Erzeugung synthetischer Trainingsdaten.
- **Wirtschaftlich:** Ein offenes, selbst entwickeltes Gerät ist günstig nachbaubar und anpassbar; eine Übertragung auf die Nutztierhaltung ist denkbar.
- **Gesellschaftlich:** Die Bewegungsüberwachung ermöglicht eine nicht-invasive Beurteilung von Gesundheit und Wohlbefinden der Tiere.

## 4 Produkteinsatz

- **Anwender:** Forschende des Labors (Konfiguration, Auslesen, Auswertung) und Tierpflegepersonal (Anlegen, Starten, Abnehmen).
- **Einsatzumfeld:** Innen- und Außengehege im Zoo; Witterung, Stöße und Scheuern sind zu erwarten.
- **Befestigung:** Halsband oder Geschirr; Tierart und damit Körpermasse und Bewegungsprofil sind noch festzulegen (O1).

## 5 Funktionale Anforderungen

Die Anforderungen beschreiben, was das Gerät können soll, nicht wie. Prioritäten:

| Prio | Stufe | Bedeutung |
|---|---|---|
| 1 | MUSS | Ohne diese Anforderung ist das Gerät für den Einsatz am Tier nicht nutzbar. |
| 2 | SOLL | Soll erfüllt werden; nicht erfüllte Punkte werden begründet. |
| 3 | KANN | Wird umgesetzt, wenn Zeit bleibt; muss später ergänzbar sein. |

| ID | Prio | Anforderung |
|---|---|---|
| F1 | 1 | Das Gerät muss die Beschleunigung in drei Achsen kontinuierlich als Rohdaten aufzeichnen. Eine Auswertung auf dem Gerät ist nicht gefordert. |
| F2 | 1 | Die Abtastrate muss im Bereich 25–100 Hz liegen. Der konkrete Wert wird aus den Anforderungen von ODBA/VeDBA und der Gangperiodizität begründet. |
| F3 | 1 | Auflösung und Messbereich müssen für ODBA/VeDBA und die Analyse der Gangperiodizität ausreichen. |
| F4 | 1 | Die Daten müssen nichtflüchtig gespeichert werden und auch bei leerer Batterie erhalten bleiben. |
| F5 | 1 | Das Gerät muss über einen für den Einsatz am Tier aussagekräftigen Zeitraum aufzeichnen. Der Zielwert wird bis Meilenstein M1 hergeleitet. |
| F6 | 1 | Die Daten müssen per Bluetooth Low Energy ausgelesen werden können, ohne das Gerät zu öffnen. |
| F7 | 1 | Die Daten müssen in einem Format vorliegen, das die Analysewerkzeuge des Labors direkt verarbeiten können. |
| F8 | 1 | Jedem Messwert muss ein Zeitpunkt zugeordnet werden können. |
| F9 | 2 | Zu Beginn der Aufnahme soll ein Synchronisationsmarker für den Abgleich mit Videoaufnahmen gesetzt werden können. |
| F10 | 2 | Die Aufnahme soll ohne Öffnen gestartet und der Zustand (Batterie, Speicher) abgefragt werden können. |
| F11 | 3 | Kompression oder reduzierte Auflösung kann die Aufzeichnungsdauer verlängern, sofern F3 erfüllt bleibt. |

## 6 Nicht-funktionale Anforderungen

| ID | Prio | Anforderung |
|---|---|---|
| NF1 | 1 | Masse und Größe müssen das Tragen an Halsband oder Geschirr erlauben. Zielwerte werden nach Festlegung der Tierart bis M1 hergeleitet. |
| NF2 | 1 | Das Gerät darf das Tier nicht gefährden (keine scharfen Kanten, keine losen Teile, gesicherte Zelle). |
| NF3 | 1 | Das Gerät muss für die gesamte Aufnahme aus seinem internen Energiespeicher betrieben werden. |
| NF4 | 1 | Spannungseinbrüche oder Neustarts dürfen bereits gespeicherte Daten nicht unbrauchbar machen. |
| NF5 | 2 | Das Gerät soll durch ein einfaches Gehäuse oder eine Schutzlackierung gegen Feuchtigkeit und mechanische Belastung geschützt sein; ein Verguss ist nicht gefordert. |
| NF6 | 2 | Das Gerät soll dokumentiert und in mehreren Exemplaren nachbaubar sein. |

## 7 Lieferumfang

**Geliefert werden:** ein funktionsfähiger Prototyp mit eigener Leiterplatte und Gehäuse bzw. Schutzbeschichtung, das KiCad-Projekt, der Quellcode von Firmware und Auslese-Werkzeug (Git), die Messprotokolle, der Datensatz der Praxisaufnahme sowie Lastenheft, Pflichtenheft, Projektbericht und Poster bzw. Extended Abstract.

**Nicht geliefert werden:** Auswertung auf dem Gerät, Live-Übertragung, eine fertige Smartphone-App, ein vergossenes Gehäuse, Zertifizierungen und eine Serienfertigung.

**Vom Auftraggeber bereitgestellt:** Entwicklungswerkzeuge und Erfahrung mit Nordic-Plattformen, Unterstützung bei Fertigung und Bestückung, Strommesstechnik, Referenzaufnahmen aus dem Vorgängerprojekt, Arbeitsplätze und der Kontakt zum Zoo.

## 8 Meilensteine

| MS | Ergebnis | Termin |
|---|---|---|
| M0 | Freigabe von Lasten- und Pflichtenheft | [Datum] |
| M1 | Zielwerte hergeleitet, Bauteile ausgewählt | [Datum] |
| M2 | Leiterplatte zur Fertigung freigegeben | [Datum] |
| M3 | Prototyp zeichnet auf und lässt sich auslesen | [Datum] |
| M4 | Messungen und Praxisaufnahme abgeschlossen | [Datum] |
| M5 | Abgabe Projektbericht und Abschlusspräsentation | [Datum] |

## 9 Offene Punkte

| Nr. | Offener Punkt | Klärung bis |
|---|---|---|
| O1 | Zieltierart und Körpermasse; daraus folgen zulässige Masse und Messbereich | M1 |
| O2 | Befestigungsart (Halsband oder Geschirr) und verfügbarer Bauraum | M1 |
| O3 | Für die Analysen benötigte Aufzeichnungsdauer und Abtastrate | M1 |
| O4 | Termin und Rahmenbedingungen einer Aufnahme im Zoo | M3 |
| O5 | Zulässigkeit des Funkbetriebs eines nicht zertifizierten Prototyps im Zoo | M1 |
| O6 | Budget, Anzahl der Exemplare, verfügbarer Code aus dem Vorgängerprojekt | M1 |
| O7 | Termine des Capstone-Projekts im WS 26/27 | M0 |

## 10 Abnahmekriterien

- Ein am Tier befestigbarer Prototyp liegt vor.
- Alle MUSS-Anforderungen sind durch Messprotokolle oder Demonstration belegt; nicht erfüllte SOLL-Anforderungen sind begründet.
- Die Daten der Praxisaufnahme sind für ODBA/VeDBA nutzbar.
- Dokumentation, KiCad-Projekt und Quellcode sind fristgerecht übergeben.
