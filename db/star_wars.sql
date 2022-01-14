CREATE DATABASE start_wars_db;
use start_wars_db;


CREATE TABLE  IF NOT EXISTS  people  (
  person_id VARCHAR(255),
  person_film_id VARCHAR(255),
  person_specy_id VARCHAR(255),
  person_vehicle_id VARCHAR(255),
  person_starship_id VARCHAR(255),
  name VARCHAR(255),
  height VARCHAR(255),
  mass VARCHAR(255),
  hair_color VARCHAR(255),
  skin_color VARCHAR(255),
  eye_color VARCHAR(255),
  birth_year VARCHAR(255),
  gender VARCHAR(255),
  homeworld VARCHAR(255),
  created VARCHAR(255),
  edited VARCHAR(255),
  url VARCHAR(255)
  );

  CREATE TABLE  IF NOT EXISTS  people_film  (
  person_film_id VARCHAR(255),
  link VARCHAR(255)
  );

  CREATE TABLE  IF NOT EXISTS  people_specy  (
  person_specy_id VARCHAR(255),
  link VARCHAR(255)
  );


  CREATE TABLE  IF NOT EXISTS  people_vehicle  (
  person_vehicle_id VARCHAR(255),
  link VARCHAR(255)
  );

  CREATE TABLE  IF NOT EXISTS  people_starship  (
  person_starship_id VARCHAR(255),
  link VARCHAR(255)
  );

CREATE TABLE IF NOT EXISTS films (
  film_id VARCHAR(255),
  film_character_id VARCHAR(255),
  film_planet_id VARCHAR(255),
  film_starship_id VARCHAR(255),
  film_vehicle_id VARCHAR(255),
  film_specy_id VARCHAR(255),
  title VARCHAR(255),
  episode_id VARCHAR(255),
  opening_crawl LONGTEXT,
  director VARCHAR(255),
  producer VARCHAR(255),
  release_date VARCHAR(255),
  created VARCHAR(255),
  edited VARCHAR(255),
  url VARCHAR(255)
);

  CREATE TABLE  IF NOT EXISTS  film_characters (
  film_character_id VARCHAR(255),
  link VARCHAR(255)
  );


  CREATE TABLE  IF NOT EXISTS  flm_planet  (
  film_planet_id VARCHAR(255),
  link VARCHAR(255)
  );



  CREATE TABLE  IF NOT EXISTS  film_starship  (
  film_starship_id VARCHAR(255),
  link VARCHAR(255)
  );

  CREATE TABLE  IF NOT EXISTS  film_vehicle  (
  film_vehicle_id VARCHAR(255),
  link VARCHAR(255)
  );

CREATE TABLE  IF NOT EXISTS  film_specy  (
  film_specy_id VARCHAR(255),
  link VARCHAR(255)
  );

CREATE TABLE IF NOT EXISTS startship (
  startship_id INT,
  name VARCHAR(255),
  model VARCHAR(255),
  starship_class VARCHAR(255),
  manufacturer VARCHAR(255),
  cost_in_credits VARCHAR(255),
  length VARCHAR(255),
  crew VARCHAR(255),
  passengers VARCHAR(255),
  max_atmosphering_speed VARCHAR(255),
  MGLT VARCHAR(255),
  cargo_capacity VARCHAR(255),
  consumables VARCHAR(255),
  url VARCHAR(255),
  created VARCHAR(255),
  edited VARCHAR(255)
  );

  CREATE TABLE IF NOT EXISTS vehicle (
  vehicle_id INT,
  name VARCHAR(255),
  model VARCHAR(255),
  vehicle_class VARCHAR(255),
  manufacturer VARCHAR(255),
  cost_in_credits VARCHAR(255),
  length VARCHAR(255),
  crew VARCHAR(255),
  passengers VARCHAR(255),
  max_atmosphering_speed VARCHAR(255),
  cargo_capacity VARCHAR(255),
  consumables VARCHAR(255),
  url VARCHAR(255),
  created VARCHAR(255),
  edited VARCHAR(255)
  );


 CREATE TABLE IF NOT EXISTS specie  (
  specie_id INT,
  name VARCHAR(255),
  classification VARCHAR(255),
  designation VARCHAR(255),
  average_height VARCHAR(255),
  average_lifespan VARCHAR(255),
  eye_colors VARCHAR(255),
  hair_colors VARCHAR(255),
  skin_colors VARCHAR(255),
  language VARCHAR(255),
  homeworld VARCHAR(255),
  url VARCHAR(255),
  created VARCHAR(255),
  edited VARCHAR(255)
  );

 CREATE TABLE IF NOT EXISTS planet  (
  planet_id INT,
  name VARCHAR(255),
  diameter VARCHAR(255),
  rotation_period VARCHAR(255),
  orbital_period VARCHAR(255),
  gravity VARCHAR(255),
  population VARCHAR(255),
  climate VARCHAR(255),
  terrain VARCHAR(255),
  surface_water VARCHAR(255),
  url VARCHAR(255),
  created VARCHAR(255),
  edited VARCHAR(255)
  );