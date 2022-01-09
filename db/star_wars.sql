CREATE DATABASE start_wars_db;
use start_wars_db;


CREATE TABLE  IF NOT EXISTS  person  (
  person_id INT,
  name VARCHAR(50),
  birth_year VARCHAR(50),
  eye_color VARCHAR(50),
  gender VARCHAR(50),
  hair_color VARCHAR(50),
  height VARCHAR(50),
  mass VARCHAR(50),
  skin_color VARCHAR(50),
  homeworld VARCHAR(50),
  url VARCHAR(50),
  created VARCHAR(50),
  edited VARCHAR(50)
  );


CREATE TABLE IF NOT EXISTS film (
  film_id INT,
  title VARCHAR(50),
  episode_id INT,
  opening_crawl VARCHAR(50),
  director VARCHAR(50),
  producer VARCHAR(50),
  release_date DATE,
  url VARCHAR(50),
  created VARCHAR(50),
  edited VARCHAR(50)

);

CREATE TABLE IF NOT EXISTS startship (
  startship_id INT,
  name VARCHAR(50),
  model VARCHAR(50),
  starship_class VARCHAR(50),
  manufacturer VARCHAR(50),
  cost_in_credits VARCHAR(50),
  length VARCHAR(50),
  crew VARCHAR(50),
  passengers VARCHAR(50),
  max_atmosphering_speed VARCHAR(50),
  MGLT VARCHAR(50),
  cargo_capacity VARCHAR(50),
  consumables VARCHAR(50),
  url VARCHAR(50),
  created VARCHAR(50),
  edited VARCHAR(50)
  );

  CREATE TABLE IF NOT EXISTS vehicle (
  vehicle_id INT,
  name VARCHAR(50),
  model VARCHAR(50),
  vehicle_class VARCHAR(50),
  manufacturer VARCHAR(50),
  cost_in_credits VARCHAR(50),
  length VARCHAR(50),
  crew VARCHAR(50),
  passengers VARCHAR(50),
  max_atmosphering_speed VARCHAR(50),
  cargo_capacity VARCHAR(50),
  consumables VARCHAR(50),
  url VARCHAR(50),
  created VARCHAR(50),
  edited VARCHAR(50)
  );


 CREATE TABLE IF NOT EXISTS specie  (
  specie_id INT,
  name VARCHAR(50),
  classification VARCHAR(50),
  designation VARCHAR(50),
  average_height VARCHAR(50),
  average_lifespan VARCHAR(50),
  eye_colors VARCHAR(50),
  hair_colors VARCHAR(50),
  skin_colors VARCHAR(50),
  language VARCHAR(50),
  homeworld VARCHAR(50),
  url VARCHAR(50),
  created VARCHAR(50),
  edited VARCHAR(50)
  );

 CREATE TABLE IF NOT EXISTS planet  (
  planet_id INT,
  name VARCHAR(50),
  diameter VARCHAR(50),
  rotation_period VARCHAR(50),
  orbital_period VARCHAR(50),
  gravity VARCHAR(50),
  population VARCHAR(50),
  climate VARCHAR(50),
  terrain VARCHAR(50),
  surface_water VARCHAR(50),
  url VARCHAR(50),
  created VARCHAR(50),
  edited VARCHAR(50)
  );