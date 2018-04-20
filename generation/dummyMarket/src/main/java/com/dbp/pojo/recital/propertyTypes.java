package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.GenPropertyTypeName;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;
import io.dummymaker.annotation.string.GenPhrase;

public class propertyTypes {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenPropertyTypeName
    private String name;
    @GenPhrase
    private String description;
}
