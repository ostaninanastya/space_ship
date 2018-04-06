create constraint on (person:Person) assert exists(person.ident); #requires neo4j entrerprise edition
create constraint on (person:Person) assert person.ident is unique;

create constraint on (department:Department) assert exists(department.ident); #requires neo4j entrerprise edition
create constraint on (department:Department) assert department.ident is unique;