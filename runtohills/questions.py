#!/usr/bin/env python
# -*- coding: utf-8 -*-

preexperiment=[
["1. Skriv inn din deltaker ID:",None,'entry'],
["2. Hvor mange kroner kan du maksimalt tjene på et fjell hvis du når toppen på dette fjellet?",None,'entry','int'],
["3. Tenkt deg at du har klatret hele veien til toppen av tre fjell. Hvor mange kroner har du da tjent total nå?"	,None,'entry','int'],
["""4. Tenk deg nå at du har klatret helt opp til toppen av tre fjell. 
På det fjerde fjellet faller du ned når du er på skritt 7. Hvor mange kroner har du opptjent nå?""",None,'entry','int'],
["""5. En urne inneholder 20 baller: 18 blå og 2 røde. Tenk deg at du trekker en ball tilfeldig av urnen 100 ganger. 
Hver gang legger du tilbake den trukne ballen og rister urnen før du trekker en ny. 
Hvor mange av de 100 ballene du trekker forventer du deg skal være røde?""",
[1]+list(range(5,105,5)),
'option'],
["""6. Tenk deg at du spiller Run to (and up) the hills! Du har fullført de forutbestemte stegene til foten av fjellet, 
og klatret 10 steg opp fjellet med en 10% sannsynlighet for at hvert steg er dårlig (2 røde og 18 blå baller i urnen). 
Anta at du velger å ta enda et steg. Hva er sannsynligheten for at du faller ned?""",
['%s%%' %i for i in [1]+list(range(5,105,5))],
'option']
]




postexperiment=[	
["1 Hvilket kjønn identifiserer du deg med?", ["Mann","Kvinne","Annet"],'option'],
["2 Hvor gammel er du?"	,("<20","20-22","23-25","26-28",">28"),'option'],
["""3 Holdning til risiko (Dohmen et al 2011) 
(0 = ikke villig til å ta risiko i det hele tatt, 10 = svært villig til å ta risiko)""",
list(range(0,11)),
'option'],
["""3.1 Hvordan ser du på deg selv, er du en person som generelt er fullstendig 
klar til å ta risiko, eller en person som prøver å unngå risiko? """,
 list(range(0,11)),
 'option'],

["""3.2. Hvordan ser du på deg selv når det kommer til å ta finansiell risiko (med penger), 
er du en person som er fullstendig klar til å ta risiko, eller en person som prøver å unngå risiko?""",
list(range(0,11)),
'option'],

["""3.3. Hvordan ser du på deg selv når det kommer til å ta risiko i sport og friluftsaktiviteter, 
er du en person som er fullstendig klar til å ta risiko, eller en person som prøver å unngå risiko? """	,
list(range(0,11)),
'option'],

["""4 I hvor mange sesonger har du vært en "aktiv toppturer"?
Med en "toppturere" mener vi en person som ferdes i eller i nærheten av skredterreng om vinteren 
(ikke kontrollerte heis-anlegg). Personen kan ferdes på ski, brett, truger, snøskuter eller lignende.  
Med "aktiv" mener vi at personen gjorde minst én tur i løpet av sesongen.	""",
["Ingen – jeg går ikke på topptur i det hele tatt",
"Mindre enn 1 sesong",
"1-2 sesonger",
"3-4 sesonger",
"5-6 sesonger",
"7-8 sesonger",
"9-10 sesonger",
"Flere enn 10 sesonger"],'option'],

["""5 Hvor mange dager per sesong går du vanligvis på topptur? Bruk en representativ 
sesong fra de siste fem sesongene. """,
["Ingen – jeg går ikke på topptur i det hele tatt",
"Mindre enn 1 dag/sesong",
"1-10 dager/sesong",
"11-20 dager/sesong",
"21-30 dager/sesong",
"31-40 dager/sesong",
"41-50 dager/sesong",
"mer enn 50 dager/sesong"],'option']
]
