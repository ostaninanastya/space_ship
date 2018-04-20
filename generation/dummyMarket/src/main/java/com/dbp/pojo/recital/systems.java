package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.id.GenId4;
import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.number.GenDouble;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;
import io.dummymaker.annotation.time.GenTime;

import java.time.LocalDate;

public class systems {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenName
    private String name;
    @GenId4
    private String type;
    @GenDouble
    private Double serialNumber;
    @GenTime(from = 2015)
    private LocalDate dateOfLaunch;
    @GenTime(from = 2015)
    private LocalDate dateOfLastChecking;
    @GenBigIdCustom
    private Integer personInCharge;
    @GenId4
    private Integer state;
}
