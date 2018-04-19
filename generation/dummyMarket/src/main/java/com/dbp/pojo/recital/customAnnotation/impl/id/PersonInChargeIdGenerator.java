package com.dbp.pojo.recital.customAnnotation.impl.id;

import io.dummymaker.generator.IGenerator;

import java.util.Random;

public class PersonInChargeIdGenerator implements IGenerator<Integer> {

    // we have 2000000 records in collection People which id starts from 1
    @Override
    public Integer generate() {
        int maxNumber = 2000000;

        Random r = new Random();
        return r.nextInt(maxNumber) + 1;
    }
}