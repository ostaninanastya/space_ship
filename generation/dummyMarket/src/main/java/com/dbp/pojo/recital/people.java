package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.id.GenId5;
import com.dbp.pojo.recital.customAnnotation.annotations.id.GenId7;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;
import io.dummymaker.annotation.string.GenPhone;

public class people {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenName
    private String name;
    @GenName
    private String surname;
    @GenName
    private String patronymic;
    @GenId5
    private Integer department;
    @GenPhone
    private String phoneNumber;
    @GenId7
    private Integer specialization;

}
