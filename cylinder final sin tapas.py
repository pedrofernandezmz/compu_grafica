from pdb import set_trace as st
from math_3d import *
from another_thing import Thing

class Cylinder(Thing):
    """ "Cylinder" está definido por el punto base, punto superior y radio.
        Cylinder(['base_point', vec3, 'cap_point', vec3, 'radius', float])
    """
    def __init__(self, pars=[]):
        super().__init__(pars)

    def intersection(self, ray):
        base = self.params['base_point']
        cap = self.params['cap_point']
        radius = self.params['radius']

        # Coordenadas correctas incluso si son negativas
        base_y, cap_y = min(base.y, cap.y), max(base.y, cap.y)

        a = (ray.dir.x)**2 + (ray.dir.z)**2
        b = 2*((ray.dir.x*ray.loc.x) - (ray.dir.x*base.x) + (ray.dir.z*ray.loc.z) - (ray.dir.z*base.z))
        c = (ray.loc.x)**2 + (base.x)**2 - (2*ray.loc.x*base.x) + (ray.loc.z)**2 + (base.z)**2 - (2*ray.loc.z*base.z) - radius**2

        D = b**2 - 4*a*c
        if D > 0:
            t1 = (-b - sqrt(D)) / (2*a)
            t2 = (-b + sqrt(D)) / (2*a)

            p1 = ray.at(t1)
            p2 = ray.at(t2)

            # Verificar si los puntos de intersección están dentro del cilindro (incluyendo las tapas)
            if base_y <= p1.y <= cap_y or base_y <= p2.y <= cap_y:
                h1 = Hit(t1, (p1 - base).normalized(), self)
                h2 = Hit(t2, (p2 - base).normalized(), self)
                return [h1, h2]
        return []

def test_cylinder():
    # Cilindro con coordenadas y alturas negativas
    cyl = Cylinder(['base_point', Vec3(-8, -3, -2), 'cap_point', Vec3(-8, 0, -2), 'radius', 2.2])
    print(cyl)

    ray = Ray(Vec3(0, 0, 0), Vec3(1, 0, 0))
    hits = cyl.intersection(ray)
    for hit in hits:
        print(hit)

def main(args):
    test_cylinder()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

