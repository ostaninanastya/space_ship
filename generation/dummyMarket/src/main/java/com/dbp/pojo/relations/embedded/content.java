package com.dbp.pojo.relations.embedded;

import com.dbp.pojo.recital.customAnnotation.annotations.GenBoatCapacityAndQuantityForRequirementContent;
import io.dummymaker.annotation.collection.GenList;
import io.dummymaker.annotation.special.GenEmbedded;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.generator.impl.EmbeddedGenerator;

import java.util.List;

public class content {
    @GenEnumerate(from = 1)
    private Integer ident;
    @GenBoatCapacityAndQuantityForRequirementContent
    private Integer quantity;
}
