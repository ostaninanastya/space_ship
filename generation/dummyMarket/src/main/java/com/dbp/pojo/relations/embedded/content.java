package com.dbp.pojo.relations.embedded;

import com.dbp.pojo.recital.customAnnotation.annotations.GenBoatCapacityAndQuantityForRequirementContent;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;

public class content {
    @GenEnumerate(from = 1)
    private Integer ident;
    @GenBoatCapacityAndQuantityForRequirementContent
    private Integer quantity;
}
