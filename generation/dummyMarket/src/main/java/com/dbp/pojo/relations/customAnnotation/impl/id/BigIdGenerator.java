package com.dbp.pojo.relations.customAnnotation.impl.id;


import io.dummymaker.generator.IGenerator;

import java.util.Random;

import static com.dbp.generate.constant.Modifier.AMOUNT;

public class BigIdGenerator implements IGenerator<Integer> {

    // we have 2000000 records in collections which id starts from 1
    @Override
    public Integer generate() {
        int maxNumber = AMOUNT;

        Random r = new Random();
        return r.nextInt(maxNumber) + 1;
    }
}