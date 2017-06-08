### Skript, das von heise.de/thema/https die Ueberschriften
### ausliest, in einen File schreibt, alle vorkommenden Woerter
### zaehlt und die 3 beliebtesten Woerter auf std.out
### ausgibt


from bs4 import BeautifulSoup
import requests
import re

outputFile = open("test.csv", "w")
outputCountFile = open("woerterCount.csv", "w")
outputFile.write("Ueberschriften\n") #Header anlegen

requestHeise  = requests.get("https://www.heise.de/thema/https")
data = requestHeise.text

soup = BeautifulSoup(data, "lxml")

content = soup.findAll("div", { "data-sourcechannel" : "security" })
woerterListe = []

for c in content:
    c = c.findAll("header")
    string = ""
    for character in c:
        character = character.text.encode('utf-8')
        character = character.decode('utf-8')  #sonst Probleme mit Sonderzeichen
        string += character
    string = string.replace("\n                 ", "\n")
    outputFile.write(string)
    woerter = re.sub("[^\w]", " ",  string).split()
    woerterListe += woerter

woerterUnique = list(set(woerterListe))
woerterCount = {}

outputCountFile.write("Wort;Anzahl\n") #Header anlegen
for wort in woerterUnique:
        count = woerterListe.count(wort)
        woerterCount[wort] = count
        line = wort+";"+str(count)+"\n"
        outputCountFile.write(line)

print("Die 3 haeufigsten Woerter:")
for i in range(0, 3):
    largest = max(woerterCount, key=lambda key: woerterCount[key])
    print(largest)
    woerterCount.pop(largest)
