CREATE DATABASE iu_test_db;
use iu_test_db;

CREATE TABLE iu_test (
  name VARCHAR(20),
  description VARCHAR(10)
);

INSERT INTO iu_test
  (name, description)
VALUES
  ('iu', 'cool'),
  ('cameroon', 'love');