package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.GenLocations;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;

public class locations {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenLocations
    private String name;

}
