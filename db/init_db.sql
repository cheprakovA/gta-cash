drop table if exists users;
create table users(
    id          integer primary key,
    username    varchar,
    lang_code   varchar,
    referral_id integer null default null,
    foreign key( referral_id ) references users( id )
);


drop table if exists items;
create table items(
    id    integer primary key, 
    title varchar, 
    price real
);


drop table if exists orders;
create table orders(
    id           integer primary key, 
    user_id      integer,
    item_id      integer,
    external_id  varchar not null,
    ud           user_data,
    tmp          temp_order,
    payed_ts     timestamp null default null,
    completed_ts timestamp null default null,
    status       varchar check( status in ('u', 'p', 'c') ) not null default 'u',
    foreign key( user_id ) references users( id ),
    foreign key( item_id ) references items( id )
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