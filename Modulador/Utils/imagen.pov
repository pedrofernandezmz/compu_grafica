// Definición de la cámara
camera {
    location <400, -1000, -300>   // Ajusta la ubicación de la cámara en el eje Z
    look_at <400, 600, 0>        // Ajusta el punto al que la cámara está mirando
    angle 45                     // Ajusta el ángulo de visión
    sky <0, 1, 0>                // Ajusta la dirección "arriba" de la cámara
}

// Definición de la luz
light_source {
    <-800, -900, 1000>
    color rgb <1, 1, 1>
}

// Definición de los objetos generados
cylinder {
    <419.2109375, 202.2265625, 0>, <419.2109375, 202.2265625, 165.51171875>, 20.763671875
    texture {
        pigment {
            color rgb <0, 1, 0>     // Color del cilindro (rojo)
        }
        finish {
            ambient 0.2             // Iluminación ambiental
            diffuse 0.8             // Iluminación difusa
        }
    }
}

sphere {
    <323.7109375, 239.24609375, -50>, 68.93070201955152
    texture {
        pigment {
            color rgb <0, 0, 1>     // Color del cilindro (rojo)
        }
        finish {
            ambient 0.2             // Iluminación ambiental
            diffuse 0.8             // Iluminación difusa
        }
    }
}

box {
    <213.71484375, 388.23046875, 320> <603.24609375, 422.234375, 280>
    texture {
        pigment {
            color rgb <1, 1, 1>     // Color del cilindro (rojo)
        }
        finish {
            ambient 0.2             // Iluminación ambiental
            diffuse 0.8             // Iluminación difusa
        }
    }
}

sphere {
    <526.73828125, 242.2421875, -50>, 70.6785775109384
    texture {
        pigment {
            color rgb <0, 0, 1>     // Color del cilindro (rojo)
        }
        finish {
            ambient 0.2             // Iluminación ambiental
            diffuse 0.8             // Iluminación difusa
        }
    }
}
