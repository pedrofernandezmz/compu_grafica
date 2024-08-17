#include "colors.inc"

camera {
    location <0, 0, 0>
    look_at <0, 0, 5>
    up <0, 1, 0>
    angle 50
}

cylinder {
    <0, 0, 0>,
    <0, 0.5, 0>, 0.1
    pigment {
        rgb <0.0, 0, 1.0>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 0.6, 0>, 0.1
    pigment {
        rgb <0.1, 0, 0.9>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 0.7, 0>, 0.1
    pigment {
        rgb <0.2, 0, 0.8>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 0.8, 0>, 0.1
    pigment {
        rgb <0.3, 0, 0.7>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 0.9, 0>, 0.1
    pigment {
        rgb <0.4, 0, 0.6>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 1.0, 0>, 0.1
    pigment {
        rgb <0.5, 0, 0.5>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 1.1, 0>, 0.1
    pigment {
        rgb <0.6, 0, 0.4>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 1.2000000000000002, 0>, 0.1
    pigment {
        rgb <0.7, 0, 0.30000000000000004>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 1.3, 0>, 0.1
    pigment {
        rgb <0.8, 0, 0.19999999999999996>
    }
}

cylinder {
    <0, 0, 0>,
    <0, 1.4, 0>, 0.1
    pigment {
        rgb <0.9, 0, 0.09999999999999998>
    }
}

light_source {
    <0, 5, 5>,
    rgb <0.9, 0.9, 0.9>
}

