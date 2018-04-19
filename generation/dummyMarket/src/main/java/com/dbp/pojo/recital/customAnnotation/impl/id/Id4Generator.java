package com.dbp.pojo.recital.customAnnotation.impl.id;

import io.dummymaker.generator.IGenerator;

import java.util.Random;

public class Id4Generator implements IGenerator<Integer> {

    //for states, system types
    @Override
    public Integer generate() {
        int maxNumber = 4;

        Random r = new Random();
        return r.nextInt(maxNumber) + 1;
    }
}