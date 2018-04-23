package com.dbp.pojo.relations;

import com.dbp.pojo.relations.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.number.GenLong;
import io.dummymaker.annotation.special.GenEnumerate;

public class person {
    @GenEnumerate(from = 1)
    private Integer ident;
    @GenBigIdCustom
    private Integer controlled;
    @GenBigIdCustom
    private Integer executor;
    @GenBigIdCustom
    private Integer headed;
    @GenBigIdCustom
    private Integer worker;
    @GenBigIdCustom
    private Integer chief;
}
