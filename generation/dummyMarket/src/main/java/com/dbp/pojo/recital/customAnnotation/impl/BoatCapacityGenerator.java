package com.dbp.pojo.recital.customAnnotation.impl;

import io.dummymaker.generator.IGenerator;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class BoatCapacityGenerator implements IGenerator<Integer> {
    //for collection boat
    @Override
    public Integer generate() {
        int maxNumber = 1000;

        Random r = new Random();
        return r.nextInt(maxNumber) + 1;
    }
}