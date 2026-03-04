create table person (
    person_id integer primary key,
    name varchar(20) not null
);

create table phone (
    phone_id integer primary key,
    person_id integer not null,
    area_code int not null,
    number int not null,
    can_recieve_sms tinyint not null,
    foreign key (person_id) references person (person_id)
);

create table address (
    address_id integer primary key,
    person_id integer not null,
    street varchar(50),
    zip integer not null
);

create table zip (
    zip integer primary key,
    city varchar(35),
    state_two_letter_code char(2)
);

create table dog (
    dog_id integer primary key,
    name varchar(35),
    breed varchar(35),
    birth_date date
);

create table award (
    award_id integer primary key,
    dog_id integer not null,
    event_date date,
    award_name varchar(25) not null,
    foreign key (dog_id) references dog (dog_id)
);

create table person_dog (
    dog_id integer,
    person_id integer,
    foreign key (dog_id) references dog (dog_id),
    foreign key (person_id) references person (person_id)
);
