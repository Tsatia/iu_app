Bewerbung Aufgabe für IU (Internationale Hochschule)

## About the project:
- I did crawl all the data (not only films). Hope this is not a problem
- Navigate to the folder where docker-compose.yml is located
- Run (sudo) docker-compose up (There is a time sleep of 50 seconds to make sure the server is running. Please be patient)
- Run (sudo) docker-compose up --build --remove-orphans 
- Run (sudo) docker-compose down to stopp all containers
- The entry point of the API is http://0.0.0.0:5000/
- e.g. http://0.0.0.0:5000/people/1 to get the data of the first person
- In the db folder you can find a snowflake schema for the db

## _Aufgabe Beschreibung:_ 

### _Data-Developer – Task_ 
Deine Aufgabe ist es **alle** Informationen (Characters, Planets, Title, Producer, …) zu den Filmen der [Star Wars API](https://swapi.dev) 
zu crawlen und zu speichern. Der Rest kann verworfen werden. Die Daten sollen in einem **„Sternschema“** oder
**„Schneeflockenschema“** transformiert und in einer **MariaDB** abgelegt werden, möglichst ohne _Doppelungen_ in den Daten.
Welches Schema besser passt, sollst du selbst entscheiden und begründen können. Die Performance ist zweitrangig, sondern
intuitive SQL-Abfragen sind wichtiger. Diese MariaDB soll mithilfe von Docker betrieben werden.

Die nun in der MariaDB gespeicherten Daten sollen durch eine Web-API durch verschiedene Endpunkte abrufbar sein. Diese kann
in Python entwickelt und mithilfe eines Frameworks (z.B. Flask) umgesetzt werden. Die Endpunkte sollen ähnlich den
Endpunkten der Star Wars API entsprechen (/films/1, /vehicles/14 oder auch /people/ um alle abzurufen). Die Web-API kann
(muss aber nicht) in einem Docker Container integriert und lauffähig sein. Gerne kann die Web-API und die MariaDB auch in
einem Docker-Compose zusammengefasst werden.
