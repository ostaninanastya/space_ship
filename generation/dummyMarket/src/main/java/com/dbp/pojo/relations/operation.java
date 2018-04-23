package com.dbp.pojo.relations;

import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import com.dbp.pojo.relations.customAnnotation.annotations.GenListOfId;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;
import io.dummymaker.annotation.time.GenTime;

import java.time.LocalDate;
import java.util.List;

public class operation {
    @GenEnumerate(from = 1)
    private Integer ident;
    @GenName
    private String name;
    @GenTime(from = 2015)
    private LocalDate start;
    @GenTime(from = 2015)
    private LocalDate end;
    @GenBigIdCustom
    private Integer department;
    @GenBigIdCustom
    private Integer requirement;
    @GenListOfId
    private List<Integer> persons;
    @GenBigIdCustom
    private Integer head;
}
