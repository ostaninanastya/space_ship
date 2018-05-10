# Space ship

Информационная система, содержащая данные о деятельности гипотетического космического корабля, отправляющегося в экспедицию на некоторую планету не-Марс.

[wiki][]

## Structure

 `/api` contains mappers and manipulators for making it possible to interact with system via [GraphQL][] as well as web-server, written on [node.js][] in order to simplify testing
 
 `/clustering` contains config files used for setting up [mongodb][], [cassandra][] and [neo4j][] clusters
 
 `/connectors` contains sets of functions for setting up connection to the databases using vendor's libraries
 
 `/generation` contatins data generators written in java for the databases; all of the generators use [dummymaker][] library
 
 `/logbook` contains code which is relevant for collections from the 'logbook' section, which represent journals
 
 `/recital` contains code which is relevant for collections from the 'recital' section, which represent basic info about the ship and it's command
 
 `/relations` contains code which is relevant for collections from the 'relations' section, which describes relations between people on the ship and introduces few extra entities
 
 `/store` contains code which is relevant for the base data container in the ilm architecture (see [wiki][] to find out more about that) - for these purposes [MySQL][] was being used
 
 `/transporters` contains modules, dedicated for exchanging data between databases in the ilm architecture

[wiki]:https://github.com/ostaninanastya/space_ship/wiki
[graphQL]:http://graphql.org/learn/
[node.js]:https://nodejs.org/en/
[mongodb]:https://www.mongodb.com/
[cassandra]:http://cassandra.apache.org/
[neo4j]:https://neo4j.com/
[MySQL]:https://www.mysql.com/
[dummymaker]:https://github.com/GoodforGod/dummymaker
