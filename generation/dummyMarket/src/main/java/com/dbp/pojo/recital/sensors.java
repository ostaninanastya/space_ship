package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.id.GenId5;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;

public class sensors {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenName
    private String name;
    @GenId5
    private Integer location;
}
