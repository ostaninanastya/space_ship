create keyspace if not exists logbook with replication = {'class' : 'SimpleStrategy', 'replication_factor' : 3};

create table cache.boats (
   id blob,
   name text,
   capacity int,
   accessed__ timestamp,
   created__ timestamp,
   gaps__ text,
   cause__ text  
   PRIMARY KEY (id_, name));

