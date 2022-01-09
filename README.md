Bewerbung Aufgabe für IU (Internationale Hochschule)

## _Aufgabe Beschreibung:_ 

### _Data-Developer – Task_ 
Deine Aufgabe ist es **alle** Informationen (Characters, Planets, Title, Producer, …) zu den Filmen der Star  [Wars API](https://swapi.dev) 
zu crawlen und zu speichern. Der Rest kann verworfen werden. Die Daten sollen in einem **„Sternschema“** oder
**„Schneeflockenschema“** transformiert und in einer **MariaDB** abgelegt werden, möglichst ohne _Doppelungen_ in den Daten.
Welches Schema besser passt, sollst du selbst entscheiden und begründen können. Die Performance ist zweitrangig, sondern
intuitive SQL-Abfragen sind wichtiger. Diese MariaDB soll mithilfe von Docker betrieben werden.

Die nun in der MariaDB gespeicherten Daten sollen durch eine Web-API durch verschiedene Endpunkte abrufbar sein. Diese kann
in Python entwickelt und mithilfe eines Frameworks (z.B. Flask) umgesetzt werden. Die Endpunkte sollen ähnlich den
Endpunkten der Star Wars API entsprechen (/films/1, /vehicles/14 oder auch /people/ um alle abzurufen). Die Web-API kann
(muss aber nicht) in einem Docker Container integriert und lauffähig sein. Gerne kann die Web-API und die MariaDB auch in
einem Docker-Compose zusammengefasst werden.
