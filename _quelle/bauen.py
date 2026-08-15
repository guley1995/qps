#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QPS – Quality Project Semiz
Website-Generator, Gestaltung „Werkplan".

Texte und Stammdaten stehen hier oben. Ändern, dann `python3 bauen.py`.
"""
import os, shutil
from stil import CSS

HIER = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HIER, "dist")

# ------------------------------------------------------------- Stammdaten
FIRMA     = "QPS – Quality Project Semiz"
INHABER   = "Mert Semiz"
DOMAIN    = "www.qps-augsburg.de"           # PLATZHALTER
TEL       = "[Telefonnummer]"               # PLATZHALTER
TEL_HREF  = "tel:+49000000000"              # PLATZHALTER
MAIL      = "[E-Mail-Adresse]"              # PLATZHALTER
MAIL_HREF = "mailto:info@example.de"        # PLATZHALTER
STRASSE   = "[Straße Hausnummer]"           # PLATZHALTER
PLZORT    = "[PLZ] Augsburg"                # PLATZHALTER
ZEITEN    = "Mo–Fr [Uhrzeit]"               # PLATZHALTER
JAHR      = "2026"

NAV = [("index.html", "Start"), ("leistungen.html", "Leistungen"),
       ("ablauf.html", "Ablauf"), ("ueber-mich.html", "Über mich"),
       ("kontakt.html", "Kontakt")]


# ------------------------------------------------------------- Bausteine
def kopf(aktiv):
    CUR = ' aria-current="page"'
    links = "".join('<a href="%s"%s>%s</a>' % (h, CUR if h == aktiv else "", t)
                    for h, t in NAV[:-1])
    return f"""<a class="sprung" href="#inhalt">Zum Inhalt</a>
<header class="kopf">
  <div class="kopf-in">
    <a class="logo" href="index.html" aria-label="{FIRMA}, Startseite">
      <span class="logo-kuerzel">QPS</span>
      <span class="logo-txt">
        <span class="logo-name">Quality Project Semiz</span>
        <span class="logo-sub">Augsburg</span>
      </span>
    </a>
    <button class="nav-schalter" id="navBtn" aria-expanded="false" aria-controls="nav">Menü</button>
    <nav class="nav" id="nav" aria-label="Hauptnavigation">
      {links}<a class="nav-cta" href="kontakt.html">Erstgespräch</a>
    </nav>
  </div>
</header>"""


def abschnitt(pos, schienentext, inhalt, klasse=""):
    return f"""
<section class="abschnitt {klasse}">
  <div class="schiene">
    <span class="pos">{pos}</span>
    <span class="pos-txt">{schienentext}</span>
  </div>
  <div class="inhalt">
{inhalt}
  </div>
</section>"""


def dim(text, rot=False):
    r = " dim-rot" if rot else ""
    return (f'<div class="dim{r}"><span class="dim-linie"></span>'
            f'<span class="dim-text">{text}</span><span class="dim-linie"></span></div>')


def liste(kopfzeilen, zeilen):
    k = ('<div class="liste-kopf"><span>%s</span><span>%s</span><span>%s</span></div>'
         % kopfzeilen)
    z = "".join(
        f'<div class="liste-zeile"><span class="lz-nr">{n}</span>'
        f'<span class="lz-titel">{t}</span><div class="lz-txt">{b}</div></div>'
        for n, t, b in zeilen)
    return f'<div class="liste">{k}{z}</div>'


def titelblock():
    return f"""<footer class="titelblock">
  <div class="tb-gitter">
    <div class="tb-zelle">
      <span class="tb-key">Betrieb</span>
      <span class="tb-val">{INHABER}<br>QPS – Quality Project Semiz<br>
      Beratung · Planung · Koordination</span>
    </div>
    <div class="tb-zelle">
      <span class="tb-key">Kontakt</span>
      <span class="tb-val"><a href="{TEL_HREF}">{TEL}</a><br>
      <a href="{MAIL_HREF}">{MAIL}</a><br>{ZEITEN}</span>
    </div>
    <div class="tb-zelle">
      <span class="tb-key">Gebiet</span>
      <span class="tb-val">Stadt Augsburg<br>Landkreis Augsburg<br>
      Aichach-Friedberg</span>
    </div>
    <div class="tb-zelle">
      <span class="tb-key">Seiten</span>
      <span class="tb-val"><ul>
        <li><a href="leistungen.html">Leistungen</a></li>
        <li><a href="ablauf.html">Ablauf</a></li>
        <li><a href="ueber-mich.html">Über mich</a></li>
        <li><a href="kontakt.html">Kontakt</a></li>
      </ul></span>
    </div>
  </div>
  <div class="tb-fuss">
    <span>© {JAHR} {INHABER}</span>
    <span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span>
  </div>
</footer>"""


NAVJS = """
<script>
(function(){
  var b=document.getElementById('navBtn'),n=document.getElementById('nav');
  if(!b||!n)return;
  b.addEventListener('click',function(){
    var o=n.classList.toggle('offen');
    b.setAttribute('aria-expanded',o?'true':'false');
    b.textContent=o?'Zu':'Men\\u00fc';
  });
})();
</script>"""

SCHEMA = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ProfessionalService",
"name":"{FIRMA}",
"description":"Unabhängige Beratung, Auswahl von Fachbetrieben und Projektkoordination für Sanierungs- und Außenbereichsprojekte in Augsburg.",
"founder":{{"@type":"Person","name":"{INHABER}"}},
"areaServed":[{{"@type":"City","name":"Augsburg"}},{{"@type":"AdministrativeArea","name":"Landkreis Augsburg"}}],
"address":{{"@type":"PostalAddress","addressLocality":"Augsburg","addressRegion":"Bayern","addressCountry":"DE"}},
"url":"https://{DOMAIN}/"}}
</script>"""


def seite(datei, titel, beschreibung, rumpf, aktiv=None):
    aktiv = aktiv if aktiv is not None else datei
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titel}</title>
<meta name="description" content="{beschreibung}">
<link rel="canonical" href="https://{DOMAIN}/{datei}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{FIRMA}">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschreibung}">
<meta property="og:locale" content="de_DE">
<meta name="theme-color" content="#F7F5EF">
<link rel="preload" href="schriften/ibm-plex-sans-condensed-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="schriften/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23F7F5EF'/><rect x='2.5' y='2.5' width='27' height='27' fill='none' stroke='%2314161A' stroke-width='1.5'/><text x='16' y='21' font-family='Helvetica' font-size='11' font-weight='bold' fill='%2314161A' text-anchor='middle'>QPS</text></svg>">
<style>{CSS}</style>
{SCHEMA}
</head>
<body>
{kopf(aktiv)}
<div class="blatt">
  <span class="passkreuz pk-lo"></span><span class="passkreuz pk-ro"></span>
  <main id="inhalt">
{rumpf}
  </main>
{titelblock()}
</div>
{NAVJS}
</body>
</html>"""
    with open(os.path.join(OUT, datei), "w", encoding="utf-8") as f:
        f.write(html)


# ------------------------------------------------------------- Seiten
def bauen():
    schriften = os.path.join(OUT, "schriften")
    tmp = None
    if os.path.isdir(schriften):
        tmp = os.path.join(HIER, "_schriften_tmp")
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.copytree(schriften, tmp)
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    if tmp:
        shutil.copytree(tmp, schriften)
        shutil.rmtree(tmp, ignore_errors=True)

    # ============================================================ START
    rumpf = f"""
<div class="titel">
  <span class="marke">Sanierung · Außenbereich · Augsburg und Landkreis</span>
  <h1>Sie planen.<br>Ich organisiere.</h1>
  <p class="titel-lead">Ich suche Ihnen die Betriebe, die für Ihr Vorhaben wirklich taugen.
  Und ich bleibe dran, bis alles steht. Ohne dass Sie zehn Nummern anrufen müssen.</p>
  {dim("Erstgespräch kostenlos · Antwort binnen 24 Stunden", rot=True)}
  <div class="tasten">
    <a class="taste taste-voll" href="kontakt.html">Vorhaben schildern</a>
    <a class="taste" href="ablauf.html">Wie das läuft</a>
  </div>
</div>
"""

    rumpf += abschnitt("01", "Bestandsaufnahme", f"""
    <div class="spalten">
      <div>
        <h2>Am Handwerk liegt es fast nie.</h2>
        <p class="gross">Es liegt an dem, was drumherum passiert. Oder eben nicht passiert.</p>
        <p class="grau">Drei Betriebe angeschrieben, von keinem eine Antwort. Zwei Angebote
        bekommen, die man nicht vergleichen kann, weil das eine Gerüst und Entsorgung enthält
        und das andere nicht. Der Elektriker kommt, bevor der Estrich raus ist. Und Sie sitzen
        abends nach der Arbeit da und sollen das sortieren.</p>
        <p class="grau">Genau diesen Teil nehme ich Ihnen ab.</p>
      </div>
      <div>
        <span class="marke marke-grau">Typische Mängelliste</span>
        <ol class="maengel">
          <li>Auf Anfragen kommt gar keine Rückmeldung</li>
          <li>Angebote sind nicht vergleichbar aufgebaut</li>
          <li>Niemand sagt, was es am Ende kostet</li>
          <li>Gewerke arbeiten in der falschen Reihenfolge</li>
          <li>Bei Rückfragen fühlt sich keiner zuständig</li>
          <li>Nach der Abnahme meldet sich niemand mehr</li>
        </ol>
      </div>
    </div>""")

    rumpf += abschnitt("02", "Leistungsumfang", f"""
    <h2>Womit ich arbeite</h2>
    <p class="gross">Zwei Bereiche, in denen ich das Netzwerk und die Erfahrung habe.
    Alles andere sage ich Ihnen ehrlich.</p>
    {liste(("Pos", "Bereich", "Umfang"), [
        ("A.1", "Sanierung &amp; Modernisierung",
         "<p>Bad, Innenausbau, Boden, Fliesen, Maler, Elektro, Heizung, Fenster, Dach, Fassade. "
         "Einzelnes Gewerk oder alles zusammen.</p>"),
        ("A.2", "Terrasse &amp; Außenbereich",
         "<p>Überdachung, Lamellendach, Markise, Pergola, Glasschiebeanlagen, Pflaster, Zaun, "
         "Gartenbau. Mein stärkster Bereich.</p>"),
        ("B.1", "Projektkoordination",
         "<p>Wenn mehrere Gewerke beteiligt sind: Reihenfolge, Termine, Kommunikation, "
         "Baustellentermine, Abnahme.</p>"),
        ("B.2", "Gutachter &amp; Sachverständige",
         "<p>Wenn erst eine unabhängige Einschätzung her muss. Bau, Immobilie, Schaden, Kfz.</p>"),
    ])}
    <div class="vermerk">
      <span class="vk">Vermerk 01 · Wichtig</span>
      <p>Ich baue nicht selbst und trete auch nicht als Generalunternehmer auf. Ihre Verträge
      schließen Sie direkt mit den ausführenden Betrieben. Das ist Absicht: So bleibe ich
      unabhängig, und Sie behalten die Entscheidung.</p>
    </div>
    <div class="tasten">
      <a class="taste" href="leistungen.html">Alle Leistungen</a>
    </div>""", "getont")

    rumpf += abschnitt("03", "Standort", """
    <div class="spalten spalten-eng">
      <div>
        <h2>Warum das hier funktioniert</h2>
      </div>
      <div>
        <p class="gross">Rund um Augsburg stehen fast 97.000 Ein- und Zweifamilienhäuser.
        Zwei Drittel davon wurden vor 1979 gebaut, also bevor es überhaupt Vorgaben zum
        Wärmeschutz gab.</p>
        <p class="grau">Das heißt: sehr viele Häuser, bei denen irgendwann etwas ansteht.
        Und sehr viele Eigentümer, die keine Zeit haben, sich durch acht Betriebe zu
        telefonieren.</p>
      </div>
    </div>
    <div class="zahlen">
      <div class="zahl"><b>96.884</b><span>Ein- und Zweifamilien-<br>häuser im Gebiet</span></div>
      <div class="zahl"><b>67 %</b><span>davon gebaut<br>vor 1979</span></div>
      <div class="zahl zahl-rot"><b>37 %</b><span>der Dachdecker antworten<br>auf eine Anfrage</span></div>
      <div class="zahl"><b>12,5</b><span>Wochen Auftragsreichweite<br>im Bauhandwerk</span></div>
    </div>
    <p class="klein" style="margin-top:18px">Quellen: Bayerisches Landesamt für Statistik 2024/25 ·
    Zensus 2022 · ZDH-Konjunkturbericht · Anfragetest Deutsche Handwerks Zeitung, Mai 2026.</p>""")

    zusagen = [
        ("Antwort binnen 24 Stunden",
         "An Werktagen. Auf jede Anfrage, auch wenn die Antwort lautet, dass ich nicht der "
         "Richtige dafür bin."),
        ("Erstgespräch kostet nichts",
         "Wir reden über Ihr Vorhaben, Ihr Budget und was realistisch ist. Danach entscheiden Sie."),
        ("Ich sage Ihnen, wer mich bezahlt",
         "Vor der Beauftragung, schriftlich. Entweder Sie oder der Betrieb. Nie beide beim "
         "selben Projekt."),
        ("Sie haben es mit mir zu tun",
         "Von der ersten Frage bis zur Abnahme. Kein Ticketsystem, keine wechselnden Namen."),
        ("Sie bleiben Vertragspartner",
         "Ihre Verträge laufen direkt mit dem Betrieb. Ich schiebe mich da nicht dazwischen."),
        ("Auch danach erreichbar",
         "Wenn nach Monaten noch was auftaucht, stehen Sie damit nicht allein da."),
    ]
    zus_html = "".join(
        f'<div class="zusage"><span class="nr">Z.{i+1:02d}</span><h3>{t}</h3><p>{b}</p></div>'
        for i, (t, b) in enumerate(zusagen))

    rumpf += abschnitt("04", "Zusagen", f"""
    <h2>Sechs Sätze, an denen<br>Sie mich messen können</h2>
    <p class="gross">„Qualität" und „Vertrauen" schreibt jeder auf seine Seite. Das hier
    kann man dagegen einhalten oder brechen.</p>
    <div class="zusagen">{zus_html}</div>""", "getont")

    rumpf += abschnitt("05", "Für Betriebe", """
    <div class="spalten">
      <div>
        <h2>Sie sind Handwerks&shy;betrieb?</h2>
        <p class="gross">Ich schicke keine Anfragen an fünf Betriebe gleichzeitig und schaue,
        wer am billigsten ist.</p>
        <p class="grau">Ich war vorher beim Kunden, ich weiß, was er will und was er ausgeben
        kann. Wenn ich Sie anrufe, ist die Sache vorgeklärt. Keine Auktion, kein verfallendes
        Guthaben, keine Jahresbindung.</p>
        <div class="tasten">
          <a class="taste" href="kontakt.html#partner">Als Partner melden</a>
        </div>
      </div>
      <div>
        <span class="marke marke-grau">Was ich erwarte</span>
        <ol class="maengel" style="counter-reset:m">
          <li>Nachweisbare Qualifikation und Versicherung</li>
          <li>Rückmeldung innerhalb von zwei Werktagen</li>
          <li>Angebote, die man lesen und vergleichen kann</li>
          <li>Termine, die halten</li>
          <li>Bescheid sagen, wenn etwas nicht klappt</li>
        </ol>
      </div>
    </div>""")

    rumpf += abschnitt("06", "Leitsatz", f"""
    <blockquote class="spruch">„Ich gebe keine Empfehlung, die ich meiner
    eigenen Familie nicht geben würde."</blockquote>
    <span class="spruch-quelle">{INHABER}, Inhaber</span>
    {dim("Erstgespräch kostenlos und unverbindlich")}
    <div class="tasten">
      <a class="taste taste-voll" href="kontakt.html">Vorhaben schildern</a>
      <a class="taste" href="{TEL_HREF}">Anrufen</a>
    </div>""", "dunkel")

    seite("index.html",
          f"{FIRMA} · Sanierung, Terrasse und Projektkoordination in Augsburg",
          "Ich suche Ihnen die passenden Fachbetriebe für Sanierung oder Außenbereich und "
          "koordiniere das Projekt bis zur Abnahme. Augsburg und Landkreis. Erstgespräch kostenlos.",
          rumpf)

    # ============================================================ LEISTUNGEN
    rumpf = """
<div class="titel">
  <span class="marke">Leistungsverzeichnis</span>
  <h1>Was ich mache.<br>Und was nicht.</h1>
  <p class="titel-lead">Beraten, auswählen, koordinieren. Gebaut wird von Betrieben,
  mit denen Sie den Vertrag direkt schließen.</p>
</div>
"""

    rumpf += abschnitt("A.1", "Sanierung", """
    <div class="spalten">
      <div>
        <h2>Sanierung &amp;<br>Modernisierung</h2>
        <p class="gross">Ob nur das Bad oder das ganze Haus: Schwierig ist selten die einzelne
        Handwerksleistung. Schwierig ist die Reihenfolge.</p>
        <p class="grau">Ich schaue mir an, was ansteht, sage Ihnen, was davon wirklich sein
        muss und was warten kann, und in welcher Reihenfolge die Gewerke ran müssen, damit
        nichts zweimal gemacht wird. Dann hole ich die passenden Betriebe dazu.</p>
        <p class="grau">Manchmal ist das Ergebnis, dass Sie weniger machen als geplant.
        Das sage ich Ihnen dann auch.</p>
      </div>
      <div>
        <span class="marke marke-grau">Gewerke</span>
        <p class="klein">Bad und Sanitär · Innenausbau · Trockenbau · Malerarbeiten ·
        Bodenbeläge · Fliesenarbeiten · Elektroinstallation · Heizung · Fenster und Türen ·
        Dacharbeiten · Fassade</p>
        <div class="vermerk">
          <span class="vk">Vermerk · Förderung</span>
          <p>Anträge für die staatliche Sanierungsförderung dürfen nur gelistete
          Energieeffizienz-Experten stellen. Wenn Ihr Vorhaben in die Richtung geht, hole ich
          einen dazu, statt so zu tun, als könnte ich das.</p>
        </div>
      </div>
    </div>""")

    rumpf += abschnitt("A.2", "Außenbereich", """
    <div class="spalten">
      <div>
        <h2>Terrasse &amp;<br>Außenbereich</h2>
        <p class="gross">Hier stecke ich am tiefsten drin. Und hier ist der Unterschied
        zwischen einem guten und einem schlechten Ergebnis am größten.</p>
        <p class="grau">Bei Terrassenüberdachungen liegen die Preise zwischen etwa 3.000 und
        20.000 Euro. Ich sage Ihnen, wo dieser Unterschied tatsächlich herkommt und wo nicht.
        Meistens entscheidet nicht das Dach, sondern das Fundament und der Anschluss ans Haus.</p>
      </div>
      <div>
        <span class="marke marke-grau">Vorhaben</span>
        <p class="klein">Terrassenüberdachung · Lamellendach · Markise · Pergola ·
        Beschattung · Glasschiebeanlagen · Wintergarten · Terrassensanierung ·
        Pflasterarbeiten · Zaunbau · Garten- und Landschaftsbau</p>
        <span class="marke marke-grau" style="margin-top:26px">Was ich vorher kläre</span>
        <ol class="maengel" style="counter-reset:m">
          <li>Braucht das eine Genehmigung oder nicht</li>
          <li>Wo sich besseres Material lohnt und wo nicht</li>
          <li>Fundament und Untergrund, der übliche Kostentreiber</li>
          <li>Entwässerung und Anschluss ans Gebäude</li>
          <li>Wie lange es wirklich dauert, inklusive Lieferzeit</li>
        </ol>
      </div>
    </div>""", "getont")

    rumpf += abschnitt("B", "Koordination", f"""
    <h2>Wenn mehrere Gewerke<br>beteiligt sind</h2>
    <p class="gross">Ab dem zweiten Gewerk entscheidet die Organisation über das Ergebnis,
    nicht der Preis.</p>
    {liste(("Pos", "Leistung", "Was das heißt"), [
        ("B.01", "Bedarf klären",
         "<p>Was muss gemacht werden, was sollte, was kann warten. Das spart oft mehr als "
         "jeder Preisvergleich.</p>"),
        ("B.02", "Ablauf und Termine",
         "<p>Wer wann arbeitet, damit keiner auf den anderen wartet.</p>"),
        ("B.03", "Angebote organisieren",
         "<p>Vergleichbare Angebote einholen und so aufbereiten, dass Sie die echten "
         "Unterschiede sehen.</p>"),
        ("B.04", "Kommunikation",
         "<p>Ein Ansprechpartner für alle. Sie müssen nicht herausfinden, warum es gerade stockt.</p>"),
        ("B.05", "Baustellentermine",
         "<p>Ich bin bei den wichtigen Terminen dabei und melde mich, bevor Sie fragen müssen.</p>"),
        ("B.06", "Abnahme und danach",
         "<p>Mängel werden aufgeschrieben und nachverfolgt. Auch nach Projektende bleibe ich "
         "Ihr Ansprechpartner.</p>"),
    ])}""")

    rumpf += abschnitt("C", "Grenzen", """
    <div class="spalten spalten-eng">
      <div>
        <h2>Was ich<br>nicht mache</h2>
        <p class="grau">Nicht aus Bescheidenheit. Für einiges davon braucht man einen
        Meisterbrief, eine Zulassung oder eine Anwaltszulassung. Ich habe keine davon,
        und ich tue auch nicht so.</p>
      </div>
      <div>
        <div class="gegen">
          <div><h3 class="nein">Selbst bauen</h3><p>Handwerksleistungen führe ich nicht aus.</p></div>
          <div><h3 class="ja">Stattdessen</h3><p>Ich suche den Betrieb, der es kann.</p></div>
          <div><h3 class="nein">Generalunternehmer sein</h3><p>Ich nehme keinen Bauauftrag an, um ihn weiterzugeben.</p></div>
          <div><h3 class="ja">Stattdessen</h3><p>Sie beauftragen direkt, ich koordiniere.</p></div>
          <div><h3 class="nein">Ihr Geld verwalten</h3><p>Ich nehme kein Baugeld entgegen und gebe keine Zahlungen frei.</p></div>
          <div><h3 class="ja">Stattdessen</h3><p>Sie zahlen die Betriebe selbst, direkt.</p></div>
          <div><h3 class="nein">Rechtsberatung</h3><p>Ob Sie Geld zurückhalten dürfen, sagt Ihnen kein Berater.</p></div>
          <div><h3 class="ja">Stattdessen</h3><p>Ich verweise an einen Anwalt, den ich kenne.</p></div>
          <div><h3 class="nein">Unfallschäden abwickeln</h3><p>Die Abwicklung mit Versicherungen gehört zum Anwalt.</p></div>
          <div><h3 class="ja">Stattdessen</h3><p>Werkstatt und Gutachter vermittle ich gern.</p></div>
        </div>
      </div>
    </div>""", "getont")

    rumpf += abschnitt("D", "Anfrage", f"""
    <h2>Klingt nach Ihrem Fall?</h2>
    <p class="gross">Schildern Sie mir kurz, worum es geht. Ein paar Sätze reichen.</p>
    {dim("Antwort binnen 24 Stunden an Werktagen")}
    <div class="tasten">
      <a class="taste taste-voll" href="kontakt.html">Vorhaben schildern</a>
      <a class="taste" href="ablauf.html">Erst den Ablauf ansehen</a>
    </div>""", "dunkel")

    seite("leistungen.html",
          "Leistungen · Sanierung, Terrasse, Projektkoordination · QPS Augsburg",
          "Sanierung und Modernisierung, Terrasse und Außenbereich, Projektkoordination und "
          "Gutachtervermittlung in Augsburg. Und was ich ausdrücklich nicht mache.",
          rumpf)

    # ============================================================ ABLAUF
    schritte = [
        ("Sie melden sich",
         "Formular, Telefon oder E-Mail. Beschreiben Sie grob, worum es geht. Mehr braucht es "
         "jetzt noch nicht."),
        ("Ich melde mich zurück",
         "An Werktagen innerhalb von 24 Stunden. Wenn ich für Ihr Vorhaben nicht der Richtige "
         "bin, sage ich das gleich."),
        ("Erstgespräch",
         "Telefonisch oder bei Ihnen. Wir klären, was Sie vorhaben, was das ungefähr kostet und "
         "ob wir zusammenpassen. Kostet nichts, verpflichtet zu nichts."),
        ("Ich schaue mir das an",
         "Vor Ort. Danach wissen Sie, was tatsächlich ansteht, in welcher Reihenfolge und mit "
         "welchem Zeitrahmen Sie rechnen müssen."),
        ("Betriebe auswählen",
         "Aus meinem Netzwerk die, die fachlich und terminlich passen. Kriterium ist die "
         "Eignung, nicht die Provision."),
        ("Angebote und Ihre Entscheidung",
         "Ich hole vergleichbare Angebote und bereite sie auf. Beauftragt wird direkt zwischen "
         "Ihnen und dem Betrieb."),
        ("Umsetzung",
         "Termine, Reihenfolge, Rückfragen, Nachträge. Ich halte die Beteiligten zusammen und "
         "sage Ihnen, wo es steht."),
        ("Abnahme",
         "Ich bin dabei, schreibe offene Punkte auf und bleibe dran, bis sie erledigt sind."),
        ("Danach",
         "Wenn in ein paar Monaten noch etwas hochkommt, rufen Sie mich an. Nicht den Betrieb."),
    ]
    schritte_html = "".join(f'<li class="schritt"><div><h3>{t}</h3><p>{b}</p></div></li>'
                            for t, b in schritte)

    rumpf = f"""
<div class="titel">
  <span class="marke">Ablaufplan</span>
  <h1>Wie das<br>abläuft.</h1>
  <p class="titel-lead">Neun Schritte, jedes Mal gleich. Damit Sie immer wissen,
  woran Sie sind und was als Nächstes kommt.</p>
</div>
"""
    rumpf += abschnitt("01", "Ablauf", f'<ol class="schritte">{schritte_html}</ol>')

    rumpf += abschnitt("02", "Vergütung", f"""
    <h2>Und wer bezahlt<br>mich dabei?</h2>
    <p class="gross">Die Frage sollte niemand erst auf der Rechnung beantwortet bekommen.
    Deshalb steht sie hier.</p>

    <div class="spalten">
      <div>
        <h3>Wenn ich nur vermittle</h3>
        <p class="grau">Ich nenne Ihnen passende Betriebe und übergebe, worum es geht.
        Danach läuft es zwischen Ihnen beiden. Das kostet Sie nichts, in dem Fall zahlt
        mir der Betrieb eine Vermittlung. Sie erfahren vorher, dass und in welcher Höhe.</p>
      </div>
      <div>
        <h3>Wenn ich das Projekt begleite</h3>
        <p class="grau">Planung, Koordination, Baustellentermine, Abnahme. Dafür zahlen Sie
        mich, als Festpreis oder nach Aufwand. Und dann nehme ich bei diesem Projekt
        kein Geld vom Betrieb. Beides gleichzeitig gibt es nicht.</p>
      </div>
    </div>

    <table class="tab">
      <thead><tr><th>Leistung</th><th>Was drin ist</th><th>Preis</th></tr></thead>
      <tbody>
        <tr><td>Erstgespräch</td><td>Bedarf klären, erste Einschätzung, Empfehlung
          zum weiteren Vorgehen</td><td class="preis">kostenlos</td></tr>
        <tr><td>Vermittlung</td><td>Passende Betriebe auswählen und den Bedarf übergeben</td>
          <td class="preis">für Sie kostenlos</td></tr>
        <tr><td>Orientierung</td><td>Termin vor Ort, Bedarfsermittlung, Betriebsempfehlung,
          bis zu drei Angebote geprüft</td><td class="preis">390 €</td></tr>
        <tr><td>Begleitung kompakt</td><td>Orientierung plus Angebote, Terminkoordination,
          ein Baustellentermin, Abnahme. Für einzelne Gewerke und Außenprojekte</td>
          <td class="preis">890 €</td></tr>
        <tr><td>Begleitung komplett</td><td>Volle Begleitung über mehrere Gewerke,
          Ablaufplanung, laufende Koordination, Mängelverfolgung, Nachbetreuung</td>
          <td class="preis">5 % der Summe<br>mind. 1.900 €</td></tr>
        <tr><td>Zusatzaufwand</td><td>Weitere Termine, Sonderleistungen nach Absprache</td>
          <td class="preis">95 € / Std.</td></tr>
      </tbody>
    </table>
    <p class="klein" style="margin-top:16px">Alle Preise netto zuzüglich Umsatzsteuer.
    Der Preis steht vor der Beauftragung schriftlich fest.</p>
    <div class="notiz">
      <p><b>Platzhalter:</b> Diese Preise vor dem Livegang bestätigen oder anpassen.</p>
    </div>""", "getont")

    rumpf += abschnitt("03", "Fragen", """
    <h2>Was ich oft<br>gefragt werde</h2>
    <div class="fragen">
      <details open><summary>Bauen Sie selbst?</summary>
        <div class="antwort"><p>Nein. Ich berate, wähle Betriebe aus und koordiniere.
        Gebaut wird von den Partnerbetrieben, mit denen Sie den Vertrag direkt schließen.
        Das ist bewusst so: Es hält mich unabhängig und Sie in der Entscheidungsposition.</p></div></details>
      <details><summary>Was kostet das Erstgespräch?</summary>
        <div class="antwort"><p>Nichts. Wenn dabei rauskommt, dass ich nicht der Richtige
        bin, sage ich das und stelle dafür auch nichts in Rechnung.</p></div></details>
      <details><summary>Arbeiten Sie auch außerhalb von Augsburg?</summary>
        <div class="antwort"><p>Schwerpunkt sind Stadt und Landkreis Augsburg sowie
        Aichach-Friedberg. Weiter draußen rede ich vorher offen darüber, ob ich dort
        überhaupt ein brauchbares Netzwerk habe. Wenn nicht, sage ich ab.</p></div></details>
      <details><summary>Bekomme ich mehrere Angebote?</summary>
        <div class="antwort"><p>In der Regel ja, und ich bereite sie so auf, dass die
        Unterschiede sichtbar werden. Ich spiele die Betriebe aber nicht gegeneinander aus.
        Wer unter Preisdruck kalkuliert, spart am Ende an der falschen Stelle, und das
        merken Sie erst hinterher.</p></div></details>
      <details><summary>Was, wenn ein Betrieb schlecht arbeitet?</summary>
        <div class="antwort"><p>Ich schreibe die Mängel auf, rede mit dem Betrieb und
        bleibe dran, bis es behoben ist. Vertragspartner sind Sie, aber Sie stehen damit
        nicht allein da. Betriebe, bei denen sich sowas wiederholt, fliegen bei mir raus.</p>
        <p>Wird es rechtlich, verweise ich an einen Anwalt. Da bastele ich nicht selbst herum.</p>
        </div></details>
      <details><summary>Machen Sie auch Förderanträge?</summary>
        <div class="antwort"><p>Nein. Für BEG-Anträge und Sanierungsfahrpläne braucht man
        die Zulassung als Energieeffizienz-Experte, und die habe ich nicht. Wenn Ihr Vorhaben
        in die Richtung geht, hole ich jemanden dazu, der sie hat.</p></div></details>
    </div>""")

    rumpf += abschnitt("04", "Kontakt", f"""
    <h2>Fangen wir<br>vorne an.</h2>
    <p class="gross">Ein paar Sätze zu Ihrem Vorhaben reichen für den Anfang.</p>
    {dim("Erstgespräch kostenlos · Antwort binnen 24 Stunden")}
    <div class="tasten">
      <a class="taste taste-voll" href="kontakt.html">Vorhaben schildern</a>
      <a class="taste" href="{TEL_HREF}">Anrufen</a>
    </div>""", "dunkel")

    seite("ablauf.html",
          "Ablauf, Preise und häufige Fragen · QPS Augsburg",
          "Von der Anfrage bis nach der Abnahme in neun Schritten. Dazu die Preise und die "
          "Antwort auf die Frage, wer QPS bezahlt.",
          rumpf)

    # ============================================================ ÜBER MICH
    rumpf = f"""
<div class="titel">
  <span class="marke">Zur Person</span>
  <h1>{INHABER}</h1>
  <p class="titel-lead">Kfz-Mechatroniker, Jahrgang 2000, aus Augsburg. Wer hier anruft,
  redet mit mir. Nicht mit einem Callcenter.</p>
</div>
"""

    rumpf += abschnitt("01", "Warum", """
    <div class="spalten">
      <div>
        <h2>Wie ich<br>dazu kam</h2>
        <p class="gross">Irgendwann fiel mir auf, dass mich ständig Leute fragen, ob ich
        jemanden kenne. Für die Heizung, fürs Bad, für die Terrasse.</p>
        <p class="grau">Nicht weil es keine Handwerker gäbe. Sondern weil man von außen nicht
        beurteilen kann, wer gut ist, was ein Angebot taugt und in welcher Reihenfolge das
        Ganze eigentlich laufen müsste. Wer den ganzen Tag arbeitet, hat dafür keine Zeit
        und keine Nerven.</p>
        <p class="grau">Aus dieser Frage ist QPS geworden. Ich mache das, was ich vorher
        nebenbei für Bekannte gemacht habe, jetzt als Beruf und richtig.</p>
      </div>
      <div>
        <span class="marke marke-grau">Was ich mitbringe</span>
        <div class="liste" style="margin-top:0">
          <div class="liste-zeile" style="grid-template-columns:1fr">
            <div><span class="lz-titel">Technisches Verständnis</span>
            <div class="lz-txt"><p>Ausbildung zum Kfz-Mechatroniker. Ich erkenne, ob ein
            Angebot plausibel ist und ob eine Erklärung stimmt.</p></div></div>
          </div>
          <div class="liste-zeile" style="grid-template-columns:1fr">
            <div><span class="lz-titel">Vertrieb und Kundengespräch</span>
            <div class="lz-txt"><p>Berufliche Erfahrung darin, Leuten zuzuhören und
            herauszufinden, was sie tatsächlich brauchen.</p></div></div>
          </div>
          <div class="liste-zeile" style="grid-template-columns:1fr">
            <div><span class="lz-titel">Ein Netzwerk vor Ort</span>
            <div class="lz-txt"><p>Betriebe in der Region, die ich persönlich kenne. Nicht
            aus einem Verzeichnis.</p></div></div>
          </div>
        </div>
        <div class="notiz">
          <p><b>Platzhalter:</b> Hier ein Porträtfoto einsetzen. Auf dieser Seite wirkt
          ein Gesicht mehr als jedes Logo.</p>
        </div>
      </div>
    </div>""")

    rumpf += abschnitt("02", "Grenzen", """
    <div class="spalten spalten-eng">
      <div>
        <h2>Was ich<br>nicht bin</h2>
      </div>
      <div>
        <p class="gross">Ich habe keinen Meisterbrief und kein Bauingenieurstudium.
        Das schreibe ich hier hin, bevor es jemand anders tut.</p>
        <p class="grau">Für das, was ich mache, brauche ich beides nicht: Ich baue nicht
        selbst und ich plane keine Statik. Ich organisiere. Aber es heißt auch, dass ich
        an bestimmten Stellen die Klappe halte und jemanden dazuhole, der es darf.
        Einen Statiker, einen Energieberater, einen Anwalt.</p>
        <p class="grau">Mir ist lieber, Sie wissen das vorher.</p>
      </div>
    </div>""", "getont")

    rumpf += abschnitt("03", "Haltung", """
    <h2>Wie ich arbeite</h2>
    <div class="zusagen">
      <div class="zusage"><span class="nr">H.01</span><h3>Erst zuhören</h3>
        <p>Ich schlage nichts vor, bevor ich verstanden habe, worum es geht und was
        das Budget hergibt.</p></div>
      <div class="zusage"><span class="nr">H.02</span><h3>Auch mal abraten</h3>
        <p>Wenn ein Vorhaben so keinen Sinn ergibt, sage ich das. Auch wenn dann kein
        Auftrag draus wird.</p></div>
      <div class="zusage"><span class="nr">H.03</span><h3>Offenlegen, wer zahlt</h3>
        <p>Vor der Beauftragung wissen Sie, ob Sie mich bezahlen oder der Betrieb.
        Beides zusammen gibt es nicht.</p></div>
      <div class="zusage"><span class="nr">H.04</span><h3>Wenige, gute Partner</h3>
        <p>Lieber ein kleines Netzwerk, auf das Verlass ist, als ein großes Verzeichnis
        ohne Aussage.</p></div>
      <div class="zusage"><span class="nr">H.05</span><h3>Nichts versprechen, was ich nicht darf</h3>
        <p>Wo eine Zulassung nötig ist, sage ich das, statt es zu überspielen.</p></div>
      <div class="zusage"><span class="nr">H.06</span><h3>Erreichbar bleiben</h3>
        <p>Auch wenn ein Projekt durch ist. Und besonders dann, wenn gerade etwas
        schiefläuft.</p></div>
    </div>""")

    rumpf += abschnitt("04", "Gebiet", """
    <div class="spalten">
      <div>
        <h2>Wo ich<br>unterwegs bin</h2>
        <p class="gross">Stadt und Landkreis Augsburg, dazu Aichach-Friedberg und die
        angrenzenden Gemeinden.</p>
        <p class="grau">Bewusst regional. Ein Netzwerk ist nur so viel wert, wie man die
        Betriebe darin persönlich kennt. Sobald das hier richtig läuft, kommen weitere
        Gebiete dazu. Vorher nicht.</p>
      </div>
      <div>
        <div class="zahlen" style="grid-template-columns:1fr 1fr">
          <div class="zahl"><b>560.000</b><span>Einwohner<br>im Gebiet</span></div>
          <div class="zahl"><b>96.884</b><span>Ein- und Zwei-<br>familienhäuser</span></div>
        </div>
      </div>
    </div>""", "getont")

    rumpf += abschnitt("05", "Leitsatz", f"""
    <blockquote class="spruch">„Ich gebe keine Empfehlung, die ich meiner
    eigenen Familie nicht geben würde."</blockquote>
    <span class="spruch-quelle">Mein Leitsatz, und daran können Sie mich festnageln</span>
    <div class="tasten">
      <a class="taste taste-voll" href="kontakt.html">Vorhaben schildern</a>
    </div>""", "dunkel")

    seite("ueber-mich.html",
          f"Über mich · {INHABER}, Augsburg",
          f"{INHABER}, Kfz-Mechatroniker aus Augsburg. Wie ich zu QPS kam, wie ich arbeite "
          "und was ich ausdrücklich nicht bin.",
          rumpf)

    # ============================================================ KONTAKT
    rumpf = f"""
<div class="titel">
  <span class="marke">Anfrage</span>
  <h1>Erzählen Sie<br>mir davon.</h1>
  <p class="titel-lead">Sie brauchen keine Pläne und keine fertige Vorstellung.
  Ein paar Sätze reichen. Ich melde mich an Werktagen innerhalb von 24 Stunden.</p>
</div>
"""

    rumpf += abschnitt("01", "Formular", """
    <div class="spalten">
      <div>
        <h2>Anfrage senden</h2>
        <form class="form" method="post" action="#" novalidate>
          <div class="feld">
            <label for="name">Name <span class="pf">*</span></label>
            <input id="name" name="name" type="text" required autocomplete="name">
          </div>
          <div class="feld">
            <label for="ort">Ort oder PLZ</label>
            <input id="ort" name="ort" type="text" autocomplete="postal-code">
          </div>
          <div class="feld">
            <label for="email">E-Mail <span class="pf">*</span></label>
            <input id="email" name="email" type="email" required autocomplete="email">
          </div>
          <div class="feld">
            <label for="tel">Telefon</label>
            <input id="tel" name="tel" type="tel" autocomplete="tel">
            <span class="hinweis">Meist der schnellste Weg für Rückfragen.</span>
          </div>
          <div class="feld voll">
            <label for="thema">Worum geht es?</label>
            <select id="thema" name="thema">
              <option value="">Bitte wählen</option>
              <option>Sanierung oder Modernisierung</option>
              <option>Bad</option>
              <option>Terrasse, Überdachung, Beschattung</option>
              <option>Außenanlage, Pflaster, Garten</option>
              <option>Mehrere Gewerke, Koordination</option>
              <option>Gutachter oder Sachverständiger</option>
              <option>Kfz-Werkstatt oder Kfz-Gutachter</option>
              <option>Etwas anderes</option>
            </select>
          </div>
          <div class="feld voll">
            <label for="nachricht">Ihr Vorhaben <span class="pf">*</span></label>
            <textarea id="nachricht" name="nachricht" required
              placeholder="Was soll gemacht werden, wo, und bis wann ungefähr?"></textarea>
          </div>
          <label class="zustimmung">
            <input type="checkbox" name="datenschutz" required>
            <span>Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen
            und bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage
            verarbeitet werden. <span class="pf">*</span></span>
          </label>
          <div class="feld voll" style="border-bottom:0;padding-top:22px">
            <div class="tasten" style="margin-top:0">
              <button class="taste taste-voll" type="submit">Absenden</button>
            </div>
          </div>
        </form>
        <div class="notiz">
          <p><b>Technischer Hinweis, vor dem Livegang entfernen:</b> Das Formular hat noch
          kein Ziel. Es braucht einen Versanddienst, zum Beispiel Formspree oder Netlify Forms.
          Danach im <code>action</code>-Attribut eintragen.</p>
        </div>
      </div>
      <div>
        <span class="marke marke-grau">Direkt</span>
        <ul class="kontakt-liste">
          <li><span class="kl">Telefon</span><span class="kv"><a href="%TELH%">%TEL%</a></span></li>
          <li><span class="kl">E-Mail</span><span class="kv"><a href="%MAILH%">%MAIL%</a></span></li>
          <li><span class="kl">Anschrift</span><span class="kv">%STR%<br>%PLZ%</span></li>
          <li><span class="kl">Zeiten</span><span class="kv">%ZEIT%</span></li>
        </ul>
      </div>
    </div>""".replace("%TELH%", TEL_HREF).replace("%TEL%", TEL)
             .replace("%MAILH%", MAIL_HREF).replace("%MAIL%", MAIL)
             .replace("%STR%", STRASSE).replace("%PLZ%", PLZORT).replace("%ZEIT%", ZEITEN))

    rumpf += abschnitt("02", "Für Betriebe", f"""
    <div class="spalten" id="partner">
      <div>
        <h2>Sie sind<br>Fachbetrieb?</h2>
        <p class="gross">Dann melden Sie sich kurz. Am besten mit zwei Sätzen zu Ihren
        Gewerken und Ihrem Einzugsgebiet.</p>
        <p class="grau">Ich baue kein großes Verzeichnis auf, sondern eine überschaubare
        Zahl von Betrieben, auf die Verlass ist. Was Sie von mir bekommen: Anfragen, bei
        denen ich vorher beim Kunden war und weiß, dass Bedarf und Budget zusammenpassen.
        Keine Auktion, keine Jahresbindung, klare Konditionen.</p>
        <div class="tasten">
          <a class="taste taste-voll" href="{MAIL_HREF}">Als Partner melden</a>
        </div>
      </div>
      <div>
        <span class="marke marke-grau">Voraussetzungen</span>
        <ol class="maengel" style="counter-reset:m">
          <li>Eintragung und Versicherungsnachweis</li>
          <li>Rückmeldung innerhalb von zwei Werktagen</li>
          <li>Angebote, die man vergleichen kann</li>
          <li>Termine, die halten</li>
          <li>Bescheid sagen, wenn etwas klemmt</li>
        </ol>
      </div>
    </div>""", "getont")

    seite("kontakt.html",
          "Kontakt · Erstgespräch kostenlos · QPS Augsburg",
          "Kontakt zu Mert Semiz, QPS Augsburg. Kostenloses und unverbindliches Erstgespräch "
          "zu Ihrem Sanierungs- oder Außenbereichsprojekt. Antwort binnen 24 Stunden.",
          rumpf)

    # ============================================================ IMPRESSUM
    rumpf = f"""
<div class="titel">
  <span class="marke">Pflichtangaben</span>
  <h1>Impressum</h1>
  <p class="titel-lead">Angaben gemäß § 5 Digitale-Dienste-Gesetz.</p>
</div>
""" + abschnitt("01", "Angaben", f"""
    <div class="notiz">
      <p><b>Vorlage, noch nicht rechtssicher.</b> Alle Platzhalter in eckigen Klammern
      müssen vor dem Livegang durch echte Angaben ersetzt werden. Ein fehlendes oder
      falsches Impressum ist abmahnfähig. Im Zweifel einmal prüfen lassen.</p>
    </div>

    <table class="tab">
      <tbody>
      <tr><td>Anbieter</td><td>{INHABER}<br>QPS – Quality Project Semiz<br>
        {STRASSE}<br>{PLZORT}<br>Deutschland</td><td></td></tr>
      <tr><td>Kontakt</td><td>Telefon: {TEL}<br>E-Mail: {MAIL}</td><td></td></tr>
      <tr><td>Umsatzsteuer-ID</td><td>[USt-IdNr. nach § 27a UStG. Falls keine vorhanden,
        diese Zeile entfernen.]</td><td></td></tr>
      <tr><td>Tätigkeit</td><td>Beratung, Vermittlung und Koordination von Bau- und
        Dienstleistungsprojekten</td><td></td></tr>
      <tr><td>Kammer</td><td>[IHK Schwaben – vor Livegang bestätigen lassen]</td><td></td></tr>
      <tr><td>Aufsicht</td><td>Ordnungsamt der Stadt Augsburg</td><td></td></tr>
      <tr><td>Inhaltlich verantwortlich</td><td>{INHABER}, Anschrift wie oben</td><td></td></tr>
      </tbody>
    </table>

    <h3 style="margin-top:44px">Streitbeilegung</h3>
    <p class="grau">Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung
    bereit: <a href="https://ec.europa.eu/consumers/odr/" rel="noopener"
    style="border-bottom:1px solid var(--rot)">ec.europa.eu/consumers/odr</a>.
    Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer
    Verbraucherschlichtungsstelle teilzunehmen.</p>

    <h3 style="margin-top:32px">Haftung für Inhalte und Links</h3>
    <p class="grau">Für eigene Inhalte auf diesen Seiten bin ich nach den allgemeinen Gesetzen
    verantwortlich. Ich bin jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde
    Informationen zu überwachen. Für die Inhalte verlinkter externer Seiten ist stets der
    jeweilige Anbieter verantwortlich.</p>

    <h3 style="margin-top:32px">Urheberrecht</h3>
    <p class="grau">Die auf diesen Seiten erstellten Inhalte unterliegen dem deutschen
    Urheberrecht.</p>""")
    seite("impressum.html", "Impressum · QPS Augsburg",
          "Impressum und Anbieterkennzeichnung.", rumpf, aktiv="")

    # ============================================================ DATENSCHUTZ
    rumpf = f"""
<div class="titel">
  <span class="marke">DSGVO</span>
  <h1>Datenschutz</h1>
  <p class="titel-lead">Informationen zur Verarbeitung personenbezogener Daten
  nach Artikel 13 DSGVO.</p>
</div>
""" + abschnitt("01", "Erklärung", f"""
    <div class="notiz">
      <p><b>Vorlage, noch nicht rechtssicher.</b> Der Text beschreibt den heutigen Stand
      dieser Website: keine externen Schriften, keine Analyse-Werkzeuge, kein Tracking,
      keine Cookies. Sobald Analytics, ein Kartendienst, Social-Media-Elemente oder ein
      externer Formulardienst dazukommen, muss der Text erweitert werden. Dann wird
      in der Regel auch ein Cookie-Banner nötig.</p>
    </div>

    <h3>1. Verantwortlich</h3>
    <p class="grau">{INHABER}, QPS – Quality Project Semiz, {STRASSE}, {PLZORT}.
    E-Mail {MAIL}, Telefon {TEL}.</p>

    <h3 style="margin-top:30px">2. Zugriffsdaten</h3>
    <p class="grau">Beim Aufruf dieser Website speichert der Hosting-Anbieter automatisch Daten
    in Server-Logfiles: aufgerufene Seite, Datum und Uhrzeit, übertragene Datenmenge,
    Browsertyp, Betriebssystem, Referrer-URL und IP-Adresse. Rechtsgrundlage ist Art. 6 Abs. 1
    lit. f DSGVO; das berechtigte Interesse liegt im sicheren und fehlerfreien Betrieb.
    Die Daten werden nach [Anzahl] Tagen gelöscht.</p>

    <h3 style="margin-top:30px">3. Kontaktaufnahme</h3>
    <p class="grau">Wenn Sie das Kontaktformular nutzen, mir schreiben oder anrufen, verarbeite
    ich Ihre Angaben ausschließlich zur Bearbeitung Ihrer Anfrage. Rechtsgrundlage ist
    Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) bzw. lit. f. Die Daten werden
    gelöscht, sobald sie nicht mehr benötigt werden und keine Aufbewahrungspflichten
    entgegenstehen.</p>

    <h3 style="margin-top:30px">4. Weitergabe an Partnerbetriebe</h3>
    <p class="grau">Zur Bearbeitung Ihrer Anfrage gebe ich die dafür erforderlichen Angaben an
    ausgewählte Partnerbetriebe weiter. Das geschieht nur, soweit es für die von Ihnen
    gewünschte Leistung nötig ist (Art. 6 Abs. 1 lit. b DSGVO), und nur an die Betriebe, die
    für Ihr Vorhaben in Frage kommen. Sie werden vorher darüber informiert.</p>

    <h3 style="margin-top:30px">5. Keine externen Dienste</h3>
    <p class="grau">Diese Website lädt keine externen Schriftarten, bindet keine Analyse- oder
    Tracking-Dienste ein und verwendet keine Social-Media-Plugins. Es werden keine Cookies zu
    Analyse- oder Werbezwecken gesetzt. Die verwendeten Schriften liegen auf demselben Server
    wie die Website.</p>

    <h3 style="margin-top:30px">6. Hosting</h3>
    <p class="grau">Diese Website wird bei [Hosting-Anbieter] gehostet. Mit dem Anbieter besteht
    ein Vertrag über Auftragsverarbeitung nach Art. 28 DSGVO.</p>

    <h3 style="margin-top:30px">7. Ihre Rechte</h3>
    <p class="grau">Sie haben das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung
    (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und
    Widerspruch (Art. 21 DSGVO). Erteilte Einwilligungen können Sie jederzeit mit Wirkung für
    die Zukunft widerrufen. Außerdem steht Ihnen ein Beschwerderecht bei einer Aufsichtsbehörde
    zu. Zuständig ist das Bayerische Landesamt für Datenschutzaufsicht, Promenade 18,
    91522 Ansbach.</p>

    <h3 style="margin-top:30px">8. Stand</h3>
    <p class="grau">[Monat Jahr]</p>""")
    seite("datenschutz.html", "Datenschutz · QPS Augsburg",
          "Datenschutzerklärung nach DSGVO.", rumpf, aktiv="")

    print("Erzeugt in", OUT)
    for f in sorted(os.listdir(OUT)):
        pfad = os.path.join(OUT, f)
        if os.path.isfile(pfad):
            print(f"   {f:24} {os.path.getsize(pfad)//1024:>4} KB")


if __name__ == "__main__":
    bauen()
