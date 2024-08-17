# gen_scenes_spiral_mandala.py

from demo_misc import Vec3

def generate_spiral_mandala():
    # Intro
    s = '#include "colors.inc"\n\n'

    # Cámara
    s += (f'camera {{\n'
          f'    location <0, 0, 5>\n'
          f'    look_at <0, 0, 0>\n'
          f'    up <0, 1, 0>\n'
          f'    angle 50\n'
          f'}}\n\n')

    # Cilindros formando una espiral mandala
    num_cylinders = 200
    spiral_radius = 0.2
    spiral_height = 0.1
    color_shift = 0.1

    for i in range(num_cylinders):
        angle = i * 137.5  # Ángulo para crear una espiral interesante
        x = spiral_radius * cos(radians(angle))
        y = spiral_radius * sin(radians(angle))

        color = f'rgb <{x + 1 + color_shift}, {y + 1 + color_shift}, {(x + y)/2 + 1 + color_shift}>'
        
        s += (f'cylinder {{\n'
              f'    <{x}, {y}, {i * spiral_height}>,\n'
              f'    <{x}, {y}, {(i + 1) * spiral_height}>, 0.01\n'
              f'    pigment {{ color {color} }}\n'
              f'}}\n\n')

    # Luz
    s += (f'light_source {{\n'
          f'    <0, 5, 5>,\n'
          f'    rgb <0.9, 0.9, 0.9>\n'
          f'}}\n\n')

    print(s)
    return s

def main(args):
    s = generate_spiral_mandala()

    with open('spiral_mandala.pov', 'w') as povf:
        povf.write(s)

    return 0

if __name__ == '__main__':
    import sys
    from math import cos, sin, radians
    sys.exit(main(sys.argv))

