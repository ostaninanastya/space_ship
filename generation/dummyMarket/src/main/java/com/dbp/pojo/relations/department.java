package com.dbp.pojo.relations;

import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.special.GenEnumerate;

public class department {
    @GenEnumerate(from = 1)
    private Integer ident;
    @GenBigIdCustom
    private Integer shifts;
    @GenBigIdCustom
    private Integer operations;
    @GenBigIdCustom
    private Integer controller;
}
