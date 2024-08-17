#include "colors.inc"
#include "woods.inc"

camera {
    location <0, 0, 0>
    look_at <10, 0, 0>
    up <0, 1, 0>
    angle 60
}

light_source {
    <4, 6, 9>,
    rgb <1, 1, 1>
}


sphere {
    <12, 0, 0>, 3
    pigment {color Yellow}
}

sphere {
    <14, 0, -5>, 2
    pigment {color Green}
}

sphere {
    <10, 0, 4>, 2
    pigment {color Orange}
}

sphere {
    <12, 3, 4>, 1.5
    pigment {color Blue}
}
