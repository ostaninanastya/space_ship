package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.GenSpecializationName;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;

public class specializations {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenSpecializationName
    private String name;
}
