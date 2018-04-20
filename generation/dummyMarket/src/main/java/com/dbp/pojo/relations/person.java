package com.dbp.pojo.relations;

import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.number.GenLong;
import io.dummymaker.annotation.special.GenEnumerate;

public class person {
    @GenEnumerate(from = 1)
    private Integer ident;

    private Integer controlled;


}
