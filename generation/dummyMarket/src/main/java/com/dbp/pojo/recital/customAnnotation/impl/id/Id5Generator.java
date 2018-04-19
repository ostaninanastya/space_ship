package com.dbp.pojo.recital.customAnnotation.impl.id;

import io.dummymaker.generator.IGenerator;

import java.util.Random;

public class Id5Generator implements IGenerator<Integer> {

    //for department, locations and propertyTypes
    @Override
    public Integer generate() {
        int maxNumber = 5;

        Random r = new Random();
        return r.nextInt(maxNumber) + 1;
    }
}