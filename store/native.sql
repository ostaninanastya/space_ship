 create database store;

 create table store.boats (
 	_id TINYBLOB, 
 	name VARCHAR(20), 
 	capacity INT, 
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50), 
 	PRIMARY KEY(_id));

 create table store.property_types (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	description VARCHAR(100),
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50),
 	PRIMARY KEY(_id(12)));

 create table store.system_states (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	description VARCHAR(100),
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50),
 	PRIMARY KEY(_id(12)));

  create table store.specializations (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50),
 	PRIMARY KEY(_id(12)));

create table store.locations (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50),
 	PRIMARY KEY(_id(12)));

create table store.sensors (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	location TINYBLOB,
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50),
 	PRIMARY KEY(_id(12)));

create table store.systems (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	type TINYBLOB,
 	serial_number FLOAT,
 	launched DATETIME,
 	checked DATETIME,
 	supervisor TINYBLOB,
 	state TINYBLOB,
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50),
 	PRIMARY KEY(_id(12)));

create table store.people (
 	_id TINYBLOB, 
 	name VARCHAR(40),
 	surname VARCHAR(40),
 	patronymic VARCHAR(40),
 	department TINYBLOB,
 	phone VARCHAR(20),
 	specialization TINYBLOB,
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50),
 	PRIMARY KEY(_id(12)));

create table store.departments (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	vk VARCHAR(100),
 	director TINYBLOB,
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50), 
 	PRIMARY KEY(_id(12)));

create table store.properties (
 	_id TINYBLOB, 
 	name VARCHAR(20),
 	type TINYBLOB,
 	admission DATETIME,
 	comissioning DATETIME,
 	department TINYBLOB,
 	__created__ DATETIME, 
 	__accessed__ DATETIME, 
 	__gaps__ BLOB, 
 	__cause__ VARCHAR(50), 
 	PRIMARY KEY(_id(12)));
