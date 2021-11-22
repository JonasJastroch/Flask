import random

adjektive = ["beste", "liebenswürdigste", "schönste", "größte"]
nomen = ["Mensch", "Hecht", "Freund", "Kumpel", "Programmierer"]

print("Du bist der ")
print(random.choice(adjektive))
print(random.choice(nomen))

#########################################

versuch = 0
gzahl = random.randint(0, 100)

while versuch < 7:
    print("Aktueller Versuch: " + str(versuch))
    versuch = versuch + 1

    zahl = int(input("Geben Sie eine Zahl zwischen 0 und 100 ein: "))

    if zahl < gzahl:
        print("Ihre Zahl ist kleiner als die gesuchte Zahl.")

    if zahl > gzahl:
        print("Ihre Zahl ist größer als die gesuchte Zahl.")

    if zahl == gzahl:
        print("Gewonnen! Sie haben die geheime Zahl gefunden: " + str(gzahl))