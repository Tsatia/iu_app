# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Run app.py when the container launches
COPY app.py /app
COPY crawling_people.py /app
COPY crawling_films.py /app
COPY crawling_starships.py /app
COPY crawling_vehicles.py  /app
COPY crawling_species.py /app
COPY crawling_planets.py /app
CMD python crawling_people.py && python crawling_planets.py && python crawling_species.py && python crawling_vehicles.py && python crawling_starships.py && python crawling_films.py && python app.py
#CMD python crawling_people.py && python app.py
