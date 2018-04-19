package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.id.GenId5;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;
import io.dummymaker.annotation.time.GenTime;

import java.time.LocalDate;

public class properties {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenName
    private String name;
    @GenId5
    private Integer type;
    @GenTime(from = 2015)
    private LocalDate dateOfAdmission;
    @GenTime(from = 2015)
    private LocalDate comissioningDate;
    @GenId5
    private Integer department;
}
