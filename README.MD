#Kawo-Rockt-Computing Tool

### Was?
Ein 'kleines' Pythontool zur Berechnung optimaler Routen nach Art des Running-Dinners (aka Rudi-Rockt!) in den Kawos

###Wie?
Man benötigt eine funktionierende Python Installation (getestet mit 3.7), sowie die Packages Pandas und Gurobi 
(bei Installationsfragen hilft das Internet). Zur Ausführung muss main.py entsprechend (z.B. via der Kommandozeile)
gestartet werden. Die Eingabedaten müssen im "input" Ordner (falls keiner da, muss man einen erstellen ) in Form
einer Excel-Tabelle (.xlsx) vorliegen und die Spalten brauchen die folgende (exakt so geschriebenen) Namen:

**team** -> Steht für die Teamnamen  
  
**zimmer** -> Die Zimmernummer in der das Team kocht  

**vorspeise, hauptspeise, nachspeise** -> Gibt die Präferenzen der Teams in Werten von 0 bis 2 an. Die höchste Präferenz
ist 0, die niedrigste 2. Beispiel: Das Team würde am liebsten die Vorspeise machen, falls das aber nicht klappt, dann
ist es egal, ob es Hauptspeise oder Nachspeise bekommt. In diesem Fall könnte man die Werte  
vorspeise = 0, hauptspeise = 1, nachspeise = 1. Gleiche Zahlen bedeuten also gleiche Präferenz. Wenn möglich stets 
niedrige Zahlen (also nicht hauptspeise =2, nachspeise = 2) verwenden, da dies einen erheblichen Einfluss auf die 
Rechendauer hat.  

**kawo** -> Gibt das Kawo als Zahl an, aus dem das Team kommt (Bei einem 'mixed' Team eines der beiden Kawos des Teams
auswählen)  

**unvertraeglichkeiten** -> Hier steht das, was die Teams als Unvertraeglichkeiten angegeben haben als Text

**email** -> Die Email-Adresse der Kontaktperson des Teams 

Ein Beispiel-Datensatz ist im input-Ordner. Außerdem muss man in der **CONFIG.txt** noch den richtigen Dateinamen 
anstelle des Beispiel-Datensatzes einfügen, damit auch der richtige Datensatz ausgewählt wird.

Nach Ausführen des Tools rechnet das erstmal eine Weile. Je nach Datensatz dauert die optimale Berechnung etwas, kann
jedoch vorzeitig abgebrochen werden (Ctr+C), der interessante Wert ist hier das "Gap", dass sehr nah an 0 sein sollte. 
Es sollte aber bei weniger als ~30 Teams zumindest 15 Minuten gewartet werden, ob das Programm nicht von selbst fertig 
wird.  

Anschließend schreibt das Tool in einen Output Ordner eine Textdatei für jedes Team, dass alle Zuteilungsinformationen
enthält (die müssen dann nur noch in die Emails eingefügt werden).

### Was noch?

Das Tool kann Routen anhand von Speisen-Präferenzen bestimmen, achtet darauf, dass es keine Raumkonflikte für Teams 
gibt, die im gleichen Zimmer kochen, und es versucht ein Zuteilung zu finden, in der man kein Team zweimal trifft 
(klappt gut), sowie möglichst alle teilnehmenden Kawos mal trifft (klappt okay). Außerdem kann es auch eine Verteilung 
der Teams finden, wenn die Zahl der Teams nicht durch 3 teilbar ist (ein feature das erlaubt, dass sich Teams freiwillig
dafür melden können, folgt irgendwann).

Sonst spuckt der Log ganz viele Sachen aus, die in den meisten Fällen nicht interessant sind, aber vielleicht lohnt sich
ja mal ein Blick in den Code ;)

###Hä?
Bei Fragen an Kevin Conrads (kevin.conrads@kawo3.rwth-aachen.de) wenden!

Viel Spaß beim Basteln

*Mehr Features folgen vielleicht in Zukunft...*