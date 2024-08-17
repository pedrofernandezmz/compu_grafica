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
    <12, 0, 0>, <12, 1, 0>, 3
    pigment {rgb <1, 1, 0>}
}

cylinder {
    <14, 3, 0>, <14, 4, 0>, 3
    pigment {rgb <0, 1, 0>}
}

cylinder {
    <14, -3, 0>, <14, -4, 0>, 3
    pigment {rgb <0, 1, 0>}
}