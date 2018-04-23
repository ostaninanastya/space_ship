package com.dbp.generate.logbook;

import com.dbp.pojo.logbook.*;
import io.dummymaker.export.IExporter;
import io.dummymaker.export.impl.CsvExporter;
import io.dummymaker.export.impl.JsonExporter;
import io.dummymaker.factory.impl.GenProduceFactory;

import java.util.ArrayList;
import java.util.List;

import static com.dbp.generate.constant.Modifier.AMOUNT;

public abstract class EnormousDataGenerator{
    public static void generate() {
        //system tests
        List<system_test> system_tests = new GenProduceFactory().produce(system_test.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./cassandra json/").withPretty().export(system_tests);

        //control action
        List<control_action> control_actions = new GenProduceFactory().produce(control_action.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./cassandra json/").withPretty().export(control_actions);

        //position
        List<position> positions = new GenProduceFactory().produce(position.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./cassandra json/").withPretty().export(positions);

        //position
        List<operation_state> operation_states = new GenProduceFactory().produce(operation_state.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./cassandra json/").withPretty().export(operation_states);

        //sensors data
        List<sensors_data> sensors_dataset = new GenProduceFactory().produce(sensors_data.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./cassandra json/").withPretty().export(sensors_dataset);

        //shift state
        List<shift_state> shift_states = new GenProduceFactory().produce(shift_state.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./cassandra json/").withPretty().export(shift_states);
    }
}
