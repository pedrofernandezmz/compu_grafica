# gen_scenes.py

from demo_misc import Vec3

def generate_cylinder_cube(nr_cylinders, radius, cylinder_height):
    phy_size = 2.2
    spacing = phy_size / (nr_cylinders - 1)
    ctr = Vec3(5, 0, 0)

    s = ''
    # Intro
    s += f'#include "colors.inc"\n\n'

    # Cámara
    s += (f'camera {{\n'
          f'    location <0, 0, 0>\n'
          f'    look_at <5, 0, 0>\n'
          f'    up <0, 1, 0>\n'
          f'    angle 50\n'
          f'}}\n\n')

    # Cilindros formando un cubo
    for x in range(nr_cylinders):
        x0 = ctr.x - phy_size / 2 + x * spacing
        xcol = x / (nr_cylinders - 1)

        for y in range(nr_cylinders):
            y0 = ctr.y - phy_size / 2 + y * spacing
            ycol = y / (nr_cylinders - 1)

            for z in range(nr_cylinders):
                z0 = ctr.y - phy_size / 2 + z * spacing
                zcol = z / (nr_cylinders - 1)
                s += (f'cylinder {{\n'
                      f'    <{x0:g}, {y0:g}, {z0:g}>,\n'
                      f'    <{x0:g}, {y0:g} + {cylinder_height:g}, {z0:g}>, {radius:g}\n'
                      f'    pigment {{\n'
                      f'        rgb <{xcol:g}, {ycol:g}, {zcol:g}>\n'
                      f'    }}\n'
                      f'}}\n\n')

    # Luz
    s += (f'light_source {{\n'
          f'    <-5, -5, -4>,\n'
          f'    rgb <0.9, 0.9, 0.9>\n'
          f'}}\n\n')

    print(s)
    return s

def main(args):
    s = generate_cylinder_cube(10, 0.05, 0.08)  # Ajusta la altura según tus necesidades
    # Puedes ajustar el número de cilindros y el radio según tus necesidades
    # s = generate_cylinder_cube(200, 0.05, 1.0)

    with open('cylinder_cube.pov', 'w') as povf:
        povf.write(s)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

