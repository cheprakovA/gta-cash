drop table if exists users;
create table users(
    id          integer primary key,
    username    varchar,
    langCode    varchar,
    referalId   integer null default null,
    foreign key( referalId ) references users( id )
);


drop table if exists items;
create table items(
    id    integer primary key, 
    title varchar, 
    price real
);


drop table if exists orders;
create table orders(
    id                 varchar not null primary key,
    userId             integer not null,
    itemId             integer not null,
    externalId         varchar not null,
    udata              userdata not null,
    status             varchar not null,
    number             varchar not null,
    amount             moneyamount not null,
    createdDateTime    timestamp not null,
    expirationDateTime timestamp not null,
    completedDateTime  timestamp null default null,
    foreign key( userId ) references users( id ),
    foreign key( itemId ) references items( id )
);


insert into items(title, price) 
values 
    ('10 million',  17.99 ),
    ('20 million',  19.99 ),
    ('25 million',  23.99 ),
    ('30 million',  27.99 ),
    ('50 million',  34.99 ),
    ('75 million',  49.99 ),
    ('100 million', 59.99 ),
    ('200 million', 79.99 ),
    ('300 million', 99.99 ),
    ('500 million', 139.99),
    ('750 million', 159.99),
    ('1 billion',   199.99);