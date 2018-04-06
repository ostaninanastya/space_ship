package space_ship;

import java.util.List;

import org.neo4j.procedure.Description;
import org.neo4j.procedure.Name;
import org.neo4j.procedure.UserFunction;

/**
 * This is an example how you can create a simple user-defined function for Neo4j.
 */
public class GetHexIdent
{
    @UserFunction
    @Description("space_ship.get_hex_ident([int1, int2]) - convert two ints to the hex identifier.")
    public String get_hex_ident(@Name("ints") List<Number> ints) {
        if (ints == null || ints.size() != 2) {
            return null;
        }
        return Long.toHexString(ints.get(0).longValue()) + Long.toHexString(ints.get(1).longValue());
    }
}