INSERT INTO person (person_id, name) VALUES
(1, 'Laura Stevenson'),
(2, 'Bob Jones'),
(3, 'Charlie Brown'),
(4, 'Jimmy Hendricks'),
(5, 'Sydney Smith'),
(6, 'Jordan Malone');

INSERT INTO phone (phone_id, person_id, area_code, number, can_recieve_sms) VALUES
(1, 1, 123, 4567890, 1),
(2, 2, 234, 5678901, 0),
(3, 3, 345, 6789012, 1),
(4, 3, 345, 6789013, 0);

INSERT INTO address (address_id, person_id, street, zip) VALUES
(1, 1, '123 Maple Street', 10001),
(2, 2, '456 Oak Road', 20002),
(3, 3, '789 Pine Avenue', 30003),
(4, 4, '119 3rd Street', 84604),
(5, 5, '121 3rd Street', 84604),
(6, 6, '123 3rd Street', 84604);

INSERT INTO zip (zip, city, state_two_letter_code) VALUES
(10001, 'New York', 'NY'),
(20002, 'Washington', 'DC'),
(30003, 'Los Angeles', 'CA'),
(84604, 'Provo', 'UT');

INSERT INTO dog (dog_id, name, breed, birth_date) VALUES
(1, 'Buddy', 'Golden Retriever', '2018-06-01'),
(2, 'Max', 'Labrador Retriever', '2019-07-15'),
(3, 'Bella', 'Poodle', '2017-08-30'),
(4, 'Rufus', 'Collie', '2017-08-30'),
(5, 'Rex', 'Corgi', '2017-08-30');

INSERT INTO award (award_id, dog_id, event_date, award_name) VALUES
(1, 1, '2021-09-20', 'Best in Show'),
(2, 1, '2020-05-10', 'Top Agility'),
(3, 3, '2021-11-05', 'Best Obedience');


INSERT INTO person_dog (dog_id, person_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 5),
(5, 5),
(5, 1),
(4, 1);
