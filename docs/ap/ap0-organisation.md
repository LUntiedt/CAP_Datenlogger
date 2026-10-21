# AP0 – Anforderungen und Organisation

| | |
|---|---|
| **Verantwortlich** | alle |
| **Zeitraum** | W1–W2, Abschluss mit M1 |
| **Bezug** | Lastenheft Abschnitt 9 (O1–O7), Pflichtenheft 2.1 |

## Ziel

Die offenen Punkte O1–O7 sind geklärt, die Zielwerte des Pflichtenhefts 2.1 sind
hergeleitet und begründet, und das Team arbeitet mit einheitlichen Werkzeugen im
gemeinsamen Repository.

## Aufgaben

### Bis M0 – Organisation

- [x] Kickoff: APs verteilen, Namen in `docs/ap/*.md`, `STATUS.md`, Lasten- und Pflichtenheft eintragen
- [x] Repository anlegen (vorerst GitHub: https://github.com/LUntiedt/CAP_Datenlogger, später ggf. GitLab der TH), `main` schützen (MR/PR + 1 Approval)
- [ ] Alle Mitglieder zum Repository hinzufügen
- [ ] Klären, ob und in welchem Umfang **Git LFS** auf GitHub genutzt werden kann (Kontingent des Kontos) → Ergebnis in `.gitattributes` umsetzen (siehe Kommentar dort)
- [ ] **KiCad-Version** festlegen und in `AGENTS.md` Abschnitt 7 eintragen
- [ ] **nRF-Connect-SDK-Version** festlegen und in `AGENTS.md` Abschnitt 8 eintragen
- [ ] Jede/r: KiCad, nRF Connect for VS Code, Git, Python installieren; Repo klonen; Firmware-Skelett für das DK bauen (`firmware/README.md`)
- [ ] O7 klären: Termine des Capstone-Projekts → Meilensteindaten in Lastenheft 8 und `STATUS.md`
- [ ] Lasten- und Pflichtenheft gemeinsam lesen, Anmerkungen per MR/PR, Freigabe durch Prof. Cremer (M0)

### Bis M1 – Zielwerte

- [ ] Stakeholder-Interview mit Prof. Cremer vorbereiten (Fragenliste aus O1–O3, O5, O6) und durchführen; Protokoll in `docs/meetings/`
- [ ] O1 Zieltierart und Körpermasse → zulässige Gerätemasse (gemeinsam mit AP5)
- [ ] O2 Befestigungsart und Bauraum (gemeinsam mit AP5)
- [ ] O3 benötigte Aufzeichnungsdauer und Abtastrate für die Analysen (gemeinsam mit AP2)
- [ ] O5 Zulässigkeit des Funkbetriebs eines nicht zertifizierten Prototyps im Zoo
- [ ] O6 Budget, Anzahl der Exemplare, verfügbarer Code aus dem Vorgängerprojekt
- [ ] Referenzaufnahmen aus dem Vorgängerprojekt beschaffen und unter `measurements/data/referenz/` ablegen (bzw. Ort dokumentieren)
- [ ] Zielwerte (Abtastrate, Auflösung, Messbereich, Aufzeichnungsdauer, Masse, Maße) mit Begründung ins Pflichtenheft eintragen → Version 1.0

## Schnittstellen

- **Liefert an alle:** festgelegte Zielwerte und Werkzeugversionen
- **Braucht von AP1/AP2/AP3:** Budgetrechnungen und Bauteildaten für die Abwägung

## Ergebnisse

- Protokolle: `docs/meetings/`
- Zielwerte: `docs/spec/pflichtenheft.md` Abschnitt 2.1

## Stand

Repository-Struktur erstellt und auf GitHub angelegt; APs verteilt und Namen eingetragen; Lasten- und Pflichtenheft 0.2 zur Abstimmung mit dem Auftraggeber.

## Offene Fragen

- Siehe O1–O7 im Lastenheft.

## Log

- 19.10.2026: Repository-Struktur angelegt.
- 21.10.2026: Teammitglieder eingetragen, Repository auf GitHub, Lasten- und Pflichtenheft auf 0.2.
