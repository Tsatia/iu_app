CREATE DATABASE iu_test_db;
use iu_test_db;

CREATE TABLE iu_test (
  name VARCHAR(100),
  description VARCHAR(100)
);

INSERT INTO iu_test
  (name, description)
VALUES
  ('iu', 'cool'),
  ('cameroon', 'love');