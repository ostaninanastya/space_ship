create keyspace if not exists logbook with replication = {'class' : 'SimpleStrategy', 'replication_factor' : 3};

create table cache.boats (
   id blob,
   name text,
   capacity int,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text  
   PRIMARY KEY (id, name));

create table cache.departments (
   id blob,
   name text,
   vk text,
   director blob,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.property_types (
   id blob,
   name text,
   description text,  
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.system_states (
   id blob,
   name text,
   description text,  
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.system_types (
   id blob,
   name text,
   description text,  
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.specializations (
   id blob,
   name text,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.locations (
   id blob,
   name text,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.sensors (
   id blob,
   name text,
   location blob,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.systems (
   id blob,
   name text,
   type blob,
   serial_number float,
   launched timestamp,
   checked timestamp,
   supervisor blob,
   state blob,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.people (
   id blob,
   name text,
   surname text,
   patronymic text,
   department blob,
   phone text,
   specialization blob,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));

create table cache.properties (
   id blob,
   name text,
   type blob,
   admission timestamp,
   comissioning timestamp,
   department blob,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text,
   PRIMARY KEY (id, name));