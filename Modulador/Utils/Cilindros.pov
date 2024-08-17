// Cámara
camera {
    location <0, -500, 0>    // Posición de la cámara arriba de los cilindros
    look_at <0, 0, 0>
}
 
// Definición de la luz
light_source {
    <10, 10, -10>           // Posición de la fuente de luz
    color rgb <1, 1, 1>     // Color de la luz (blanco)
}

// Cilindro
cylinder {
    <345.23828125, 146.7265625, 0>, <345.23828125, 146.7265625, 259.0>, 29.994140625
    texture {
        pigment {
            color rgb <1, 0, 0>     // Color del cilindro (rojo)
        }
        finish {
            ambient 0.2             // Iluminación ambiental
            diffuse 0.8             // Iluminación difusa
        }
    }
}

// Cilindro adicional
cylinder {
    <266.7109375, 287.2421875, 0>, <266.7109375, 287.2421875, 122.49609375>, 113.509765625
    texture {
        pigment {
            color rgb <0, 0, 1>     // Color del cilindro adicional (azul)
        }
        finish {
            ambient 0.2             // Iluminación ambiental
            diffuse 0.8             // Iluminación difusa
        }
    }
}



