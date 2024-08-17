from math_3d import Vec3

def main():
    # Crear una instancia de Vec3
    v1 = Vec3(2, 3, 4)
    v2 = Vec3(5, 6, 7)

    # Calcular y mostrar la longitud al cuadrado
    dot_product = v1.dot(v2)
    print(dot_product)

if __name__ == "__main__":
    main()
