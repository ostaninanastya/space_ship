CREATE OR REPLACE FUNCTION sin (input double) 
CALLED ON NULL INPUT 
RETURNS double LANGUAGE javascript AS
'Math.sin(input);';

CREATE OR REPLACE FUNCTION cos (input double) 
CALLED ON NULL INPUT 
RETURNS double LANGUAGE javascript AS
'Math.cos(input);';

CREATE OR REPLACE FUNCTION get_x_speed (speed double, attack_angle double, direction_angle double) 
CALLED ON NULL INPUT 
RETURNS double LANGUAGE javascript AS
'speed * Math.cos(attack_angle) * Math.cos(direction_angle);';
