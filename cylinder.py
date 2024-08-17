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

        # Intersección con las paredes del cilindro
        a = (ray.dir.x)**2 + (ray.dir.z)**2
        b = 2*((ray.dir.x*ray.loc.x) - (ray.dir.x*base.x) + (ray.dir.z*ray.loc.z) - (ray.dir.z*base.z))
        c = (ray.loc.x)**2 + (base.x)**2 - (2*ray.loc.x*base.x) + (ray.loc.z)**2 + (base.z)**2 - (2*ray.loc.z*base.z) - radius**2

        D = b**2 - 4*a*c
        hits_walls = []

        if D > 0:
            t1 = (-b - sqrt(D)) / (2*a)
            t2 = (-b + sqrt(D)) / (2*a)

            p1 = ray.at(t1)
            p2 = ray.at(t2)

            # Verificar si los puntos de intersección están dentro del cilindro (sin incluir las tapas)
            if base_y <= p1.y <= cap_y:
                h1 = Hit(t1, (p1 - base).normalized(), self)
                hits_walls.append(h1)

            if base_y <= p2.y <= cap_y:
                h2 = Hit(t2, (p2 - base).normalized(), self)
                hits_walls.append(h2)

        # Intersección con las tapas
        t1_cap = (cap.y - ray.loc.y) / ray.dir.y
        t2_cap = (base.y - ray.loc.y) / ray.dir.y

        hits_caps = []

        if t1_cap >= 0:
            p1_cap = ray.at(t1_cap)
            if (p1_cap.x - base.x)**2 + (p1_cap.z - base.z)**2 <= radius**2:
                h1_cap = Hit(t1_cap, Vec3(0, -1, 0), self)
                hits_caps.append(h1_cap)

        if t2_cap >= 0:
            p2_cap = ray.at(t2_cap)
            if (p2_cap.x - base.x)**2 + (p2_cap.z - base.z)**2 <= radius**2:
                h2_cap = Hit(t2_cap, Vec3(0, 1, 0), self)
                hits_caps.append(h2_cap)

        return hits_walls + hits_caps

def test_cylinder():
    # Cilindro con coordenadas y alturas positivas
    cyl2 = Cylinder(['base_point', Vec3(8, 0, 0), 'cap_point', Vec3(8, 3, 0), 'radius', 2.2])
    print(cyl2)

    ray2 = Ray(Vec3(8, 0, 0), Vec3(8, 3, 0))
    hits2 = cyl2.intersection(ray2)
    for hit in hits2:
        print(hit)

def main(args):
    test_cylinder()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

