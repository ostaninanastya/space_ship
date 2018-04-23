package com.dbp.pojo.relations.customAnnotation.impl;


import io.dummymaker.generator.IGenerator;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import static com.dbp.generate.constant.Modifier.AMOUNT;

public class ListOfIdGenerator implements IGenerator<List<Integer>> {

    // we have 2000000 records in collections which id starts from 1
    @Override
    public List<Integer> generate() {
        int maxNumber = AMOUNT;
        List<Integer> listOfId = new ArrayList<Integer>();
        Random r = new Random();
        int maxCount = r.nextInt(10) + 1;

        for (int i = 0; i < maxCount; i++) {
            listOfId.add(r.nextInt(maxNumber) + 1);
        }
        return listOfId;
    }
}