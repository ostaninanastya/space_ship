package com.dbp.pojo.recital.customAnnotation.impl.id;

import io.dummymaker.generator.IGenerator;
import java.util.Random;

public class BigIdGenerator implements IGenerator<Integer> {

    // we have 2000000 records in collections which id starts from 1
    @Override
    public Integer generate() {
        int maxNumber = com.dbp.generate.LargeDataGenerator.AMOUNT;

        Random r = new Random();
        return r.nextInt(maxNumber) + 1;
    }
}