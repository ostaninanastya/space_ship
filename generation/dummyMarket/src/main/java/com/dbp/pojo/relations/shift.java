package com.dbp.pojo.relations;

import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;
import io.dummymaker.annotation.time.GenTime;

import java.time.LocalDate;

public class shift {
    @GenEnumerate(from = 1)
    private Integer ident;
    @GenTime(from = 2015)
    private LocalDate start;
    @GenTime(from = 2015)
    private LocalDate end;
    @GenBigIdCustom
    private Integer department;

}
