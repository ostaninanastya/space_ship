 create database store;

 create table boats (_id TINYBLOB, name VARCHAR(20), capacity INT, __created__ DATETIME, __accessed__ DATETIME, __gaps__ BLOB, __cause__ VARCHAR(50), PRIMARY KEY(_id))