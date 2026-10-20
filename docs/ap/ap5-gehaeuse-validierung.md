# AP5 – Gehäuse und Validierung

| | |
|---|---|
| **Verantwortlich** | [Name 5] |
| **Zeitraum** | W2–W6 (Gehäuse), W8–W10 (Validierung) |
| **Bezug** | F3, F9, NF1, NF2, NF5 · Pflichtenheft 3.1, 2.5 (Validierung) |
| **Dateien** | `hardware/enclosure/`, `measurements/` |

## Ziel

Das Gerät lässt sich sicher am Tier befestigen, ist gegen Feuchtigkeit und
mechanische Belastung geschützt, und eine erste Praxisaufnahme belegt, dass die
Daten für ODBA/VeDBA nutzbar sind.

## Aufgaben

### Bis M1 – Anforderungen an die Mechanik

- [ ] Mit AP0 Tierart, Körpermasse und Befestigung klären (O1, O2) → zulässige Masse und Maße des Geräts
- [ ] Weckmechanismus mit AP2 entscheiden (Reed-Kontakt vs. Bewegungsmuster) – Auswirkung auf das Gehäuse
- [ ] Schutzkonzept: 3D-gedrucktes Gehäuse vs. Schutzlackierung (NF5), ADR

### Bis M2 – Gehäuseentwurf

- [ ] Gehäuse mit Befestigung für Halsband oder Geschirr entwerfen (CAD unter `hardware/enclosure/`), Platinenumriss von AP4 übernehmen
- [ ] Anforderungen an das Gehäuse: keine scharfen Kanten, keine losen Teile, gesicherte Zelle (NF2), Zellwechsel möglich, Antennenbereich frei von Metall, Achsrichtungen außen markiert
- [ ] Ersten Druck mit Dummy-Platine prüfen

### Bis M3 – Fertiges Gehäuse

- [ ] Gehäuse mit Prototyp montieren, Masse wiegen (NF1)
- [ ] Mechanische Tests (Fall, Stoß, Scheuern) und Feuchtigkeitstest planen und durchführen, Protokoll in `measurements/protocols/`

### Bis M4 – Validierung

- [ ] Signalqualität gegenüber den Referenzaufnahmen des Vorgängerprojekts vergleichen (gleiche Bewegung mit beiden Geräten)
- [ ] Praxisaufnahme planen: Zoo (O4) oder ersatzweise Testobjekt; Ablauf nach Pflichtenheft 3.7 mit Videoaufnahme und Sync-Marker
- [ ] Praxisaufnahme durchführen, Daten mit `tools/readout/` auslesen, ODBA/VeDBA berechnen und Nutzbarkeit bewerten
- [ ] Datensatz und Protokoll unter `measurements/` ablegen

## Schnittstellen

- **Braucht:** Platinenmaße (AP4), Zellenmaße (AP1), Auslesewerkzeug (AP3), Referenzaufnahmen (AP0)
- **Liefert:** Gehäusemaße an AP4, Validierungsergebnisse an AP6

## Ergebnisse

- Gehäuse: `hardware/enclosure/`
- Protokolle und Daten: `measurements/`

## Stand

Nicht begonnen.

## Offene Fragen

- 

## Log

- 
