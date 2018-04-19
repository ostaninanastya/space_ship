package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.GenSystemTypes;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenPhrase;

public class systemTypes {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenSystemTypes
    private String name;
    @GenPhrase
    private String description;
}
