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

        return hits_caps


def test_cylinder():
    cyl = Cylinder(['base_point', Vec3(8, 0, 0), 'cap_point',
                   Vec3(8, 3, 0), 'radius', 2.2])
    print(cyl)

    ray = Ray(Vec3(8, 0, 0), Vec3(8, 3, 0))
    hits = cyl.intersection(ray)
    for hit in hits:
        print(hit)


def main(args):
    test_cylinder()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

