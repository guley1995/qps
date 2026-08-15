# QPS-Website

Fünf Seiten plus Impressum und Datenschutz. Läuft ohne Server: `index.html` doppelklicken.

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite |
| `leistungen.html` | Sanierung, Außenbereich, Koordination, und was nicht gemacht wird |
| `ablauf.html` | Ablauf in 9 Schritten, Preise, häufige Fragen |
| `ueber-mich.html` | Person, Haltung, Einzugsgebiet |
| `kontakt.html` | Formular, Kontaktdaten, Partnerbereich |
| `impressum.html` | **Vorlage, muss vervollständigt werden** |
| `datenschutz.html` | **Vorlage, muss vervollständigt werden** |
| `schriften/` | Die Schriftdateien. Nicht löschen, sonst sieht die Seite anders aus. |
| `_quelle/` | Die Bauskripte, falls du größere Änderungen machen willst |

---

## Vor dem Livegang

**Alles in eckigen Klammern ersetzen.** Die Platzhalter stehen bewusst drin, damit
nichts Erfundenes online geht:

- Telefonnummer, E-Mail, Anschrift, Erreichbarkeitszeiten
- Preise im Abschnitt „Vergütung" auf `ablauf.html`
- Impressum: Anschrift, USt-IdNr. oder Steuernummer, zuständige Kammer
- Datenschutz: Hosting-Anbieter, Löschfrist der Logfiles, Stand-Datum

Schnellster Weg: Suchen-und-Ersetzen über alle Dateien. Sauberer: oben in
`_quelle/bauen.py` die Stammdaten ändern und `python3 bauen.py` laufen lassen.

**Das Kontaktformular hat noch kein Ziel** (`action="#"`). Beim Absenden passiert nichts.
Einfachste Lösungen: Formspree, Netlify Forms oder ein PHP-Skript beim Hoster. Danach
den Hinweiskasten darunter löschen.

**Porträtfoto** auf `ueber-mich.html` einsetzen. Auf einer Seite, die von Vertrauen lebt,
wirkt ein Gesicht mehr als jedes Logo.

---

## Wichtig wegen dem Gründungszuschuss

**Die Seite darf erst online, wenn der Antrag bewilligt ist.**

Eine öffentlich erreichbare Website mit Leistungsangebot ist eine vorbereitende Handlung
mit Außenwirkung. Die kann als Aufnahme der selbstständigen Tätigkeit gewertet werden, und
der Antrag muss vorher gestellt sein (§ 324 Abs. 1 SGB III). Wenn das schiefgeht, ist der
Zuschuss weg, und zwar endgültig.

Gleiches gilt für Google Ads, Instagram-Posts und Visitenkarten verteilen. Erst der
Antrag, dann alles andere. Steht auch so im Businessplan, Kapitel 11.1.

---

## Was an dieser Seite bewusst so ist

**Keine externen Dienste.** Kein Google Fonts, kein Analytics, kein Tracking, keine
Cookies. Die Schriften liegen im Ordner `schriften/` und werden vom eigenen Server
geladen. Deshalb braucht die Seite **kein Cookie-Banner**, und die Datenschutzerklärung
bleibt kurz. Google Fonts nachträglich einzubinden wäre in Deutschland ein bekanntes
Abmahnrisiko.

Sobald Analytics, Google Maps oder Social-Plugins dazukommen, müssen Datenschutzerklärung
**und** Cookie-Banner nachgezogen werden.

**Die Gestaltung ist an eine technische Zeichnung angelehnt.** Millimeterraster im
Hintergrund, Positionsnummern am Rand, Bemaßungslinien, und die Fußzeile ist ein
Schriftfeld wie auf einem Bauplan. Das passt inhaltlich zu Planung und Koordination und
sieht nach niemandem sonst aus. Deshalb keine Kacheln, keine Icons, keine Farbverläufe.

**Alles ist in der Ich-Form geschrieben.** Kein „wir", weil da erstmal niemand ist außer
dir. Ein Einzelunternehmer, der das auch zugibt, wirkt glaubwürdiger als eine Ein-Mann-Firma,
die wie eine Agentur klingt. Und es ist schwerer zu kopieren.

**Der Fokus liegt auf Sanierung und Außenbereich.** Kfz, Reinigung, Umzug und IT stehen
nirgends prominent. Eine Seite, die alles anbietet, wirkt bei niemandem kompetent und
rankt bei Google für nichts. Die anderen Bereiche kommen dazu, wenn sie laufen.

**Es steht offen drauf, wer QPS bezahlt** (`ablauf.html`). Ungewöhnlich, und genau deshalb
ein Unterscheidungsmerkmal gegenüber Portalen, wo man das erst im Kleingedruckten findet.
Rechtlich ist die Offenlegung ohnehin die sichere Variante, wenn Provisionen fließen.

**Es steht drauf, dass QPS nicht selbst baut** und dass der Kunde seine Verträge direkt
mit den Betrieben schließt. Das ist die wichtigste Aussage auf der ganzen Seite: Sie hält
dich aus der Handwerksrollenpflicht und der Generalunternehmerhaftung raus. Bitte nicht
wegkürzen.

**Statt „Qualität, Vertrauen, Zuverlässigkeit" stehen sechs Zusagen da**, die man auch
brechen kann. Adjektive schreibt die Konkurrenz auch. Überprüfbare Versprechen nicht.

---

## Technisches

- SEO ist vorbereitet: eigene Titel und Beschreibungen pro Seite, saubere Überschriften­struktur,
  `LocalBusiness`-Auszeichnung für Google, Open-Graph-Tags fürs Teilen.
- Barrierefrei nutzbar: Tastaturbedienung, sichtbare Fokusrahmen, Sprunglink, ausreichende
  Kontraste, funktioniert ab 320 px Breite.
- Gesamtgröße rund 400 KB inklusive Schriften. Lädt auch bei schlechtem Empfang schnell.

## Online stellen

1. Domain sichern. Vorher kurz beim DPMA prüfen, ob „QPS" markenrechtlich frei ist,
   das Kürzel ist mehrfach belegt.
2. Hosting mit SSL. 10 bis 60 Euro im Jahr reichen für diese Seite völlig.
3. Alle Dateien inklusive Ordner `schriften/` per FTP hochladen. Fertig.
4. Google-Unternehmensprofil anlegen, kostenlos. Bringt für lokale Suchanfragen mehr
   als jede Anzeige.
5. Seite in der Google Search Console anmelden.
