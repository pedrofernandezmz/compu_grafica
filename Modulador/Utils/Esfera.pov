// Escena POV-Ray con tres esferas

// Configuración de la cámara
camera {
    location <0, 1200, -800>    // Posición de la cámara
    look_at <0, 0, 0>       // Punto al que mira la cámara
}

// Fuente de luz
light_source {
    <-1300, -100, -100>           // Posición de la fuente de luz
    color rgb <1, 1, 1>     // Color de la luz (blanco)
}

// Esfera
sphere {
    <419.23828125, 276.234375, 0>, 244.39801722469898
    texture {
        pigment {
            color rgb <0, 1, 0>     // Color de la esfera 2 (verde)
        }
        finish {
            ambient 0.2             // Iluminación ambiental
            diffuse 0.8             // Iluminación difusa
        }
    }
}



