#include "colors.inc"
#include "woods.inc"

camera {
    location <0, 0, 0>
    look_at <10, 0, 0>
    up <0, 1, 0>
    angle 60
}

light_source {
    <-4, 6, 9>,
    rgb <1, 1, 1>
}


cylinder {
    <14, 3, 3>, <12, 4, 3>, 1
    pigment {rgb <1, 0, 0>}
}

cylinder {
    <14, 3, 0>, <14, 4, 0>, 1
    pigment {rgb <1, 0.5, 0>}
}

cylinder {
    <14, 3, -3>, <14, 4, -3>, 1
    pigment {rgb <1, 1, 0>}
}



cylinder {
    <14, 0, 3>, <12, 1, 3>, 1
    pigment {rgb <0, 1, 0>}
}

cylinder {
    <14, 0, 0>, <14, 1, 0>, 1
    pigment {rgb <0, 1, 0.5>}
}

cylinder {
    <14, 0, -3>, <14, 1, -3>, 1
    pigment {rgb <0, 1, 1>}
}



cylinder {
    <14, -3, 3>, <12, -2, 3>, 1
    pigment {rgb <0, 0, 1>}
}

cylinder {
    <14, -3, 0>, <14, -2, 0>, 1
    pigment {rgb <0.5, 0, 1>}
}

cylinder {
    <14, -3, -3>, <14, -2, -3>, 1
    pigment {rgb <1, 0, 1>}
}







cylinder {
    <17, 3, 3>, <12, 4, 3>, 1
    pigment {rgb <1, 0.5, 0>}
}

cylinder {
    <17, 3, 0>, <14, 4, 0>, 1
    pigment {rgb <1, 1, 0>}
}

cylinder {
    <17, 3, -3>, <14, 4, -3>, 1
    pigment {rgb <0, 1, 0>}
}



cylinder {
    <17, 0, 3>, <12, 1, 3>, 1
    pigment {rgb <0, 1, 0.5>}
}

cylinder {
    <17, 0, 0>, <14, 1, 0>, 1
    pigment {rgb <0, 1, 1>}
}

cylinder {
    <17, 0, -3>, <14, 1, -3>, 1
    pigment {rgb <0, 0, 1>}
}



cylinder {
    <17, -3, 3>, <12, -2, 3>, 1
    pigment {rgb <0.5, 0, 1>}
}

cylinder {
    <17, -3, 0>, <14, -2, 0>, 1
    pigment {rgb <1, 0, 1>}
}

cylinder {
    <17, -3, -3>, <14, -2, -3>, 1
    pigment {rgb <1, 0, 0>}
}






cylinder {
    <20, 3, 3>, <12, 4, 3>, 1
    pigment {rgb <1, 1, 0>}
}

cylinder {
    <20, 3, 0>, <14, 4, 0>, 1
    pigment {rgb <0, 1, 0>}
}

cylinder {
    <20, 3, -3>, <14, 4, -3>, 1
    pigment {rgb <0, 1, 0.5>}
}



cylinder {
    <20, 0, 3>, <12, 1, 3>, 1
    pigment {rgb <0, 1, 1>}
}

cylinder {
    <20, 0, 0>, <14, 1, 0>, 1
    pigment {rgb <0, 0, 1>}
}

cylinder {
    <20, 0, -3>, <14, 1, -3>, 1
    pigment {rgb <0.5, 0, 1>}
}



cylinder {
    <20, -3, 3>, <12, -2, 3>, 1
    pigment {rgb <1, 0, 1>}
}

cylinder {
    <20, -3, 0>, <14, -2, 0>, 1
    pigment {rgb <1, 0, 0>}
}

cylinder {
    <20, -3, -3>, <14, -2, -3>, 1
    pigment {rgb <1, 0.5, 0>}
}