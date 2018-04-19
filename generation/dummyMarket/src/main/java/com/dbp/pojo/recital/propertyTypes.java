package com.dbp.pojo.recital;

import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenPhrase;

public class propertyTypes {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenPhrase
    private String description;
}
