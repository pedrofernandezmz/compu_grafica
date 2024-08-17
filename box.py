from math_3d import *
from another_thing import Thing

class Box(Thing):
    def __init__(self, corner1, corner2):
        super().__init__({'corner1': corner1, 'corner2': corner2})

    def intersection(self, ray):
        corner1 = self.params['corner1']
        corner2 = self.params['corner2']

        Tnear = float('-inf')
        Tfar = float('inf')

        for i in range(3):
            if ray.dir[i] == 0:
                # Ray is parallel to the plane
                if ray.loc[i] < corner1[i] or ray.loc[i] > corner2[i]:
                    return []  # No intersection

            # Compute intersection distance of the planes
            T1 = (corner1[i] - ray.loc[i]) / ray.dir[i]
            T2 = (corner2[i] - ray.loc[i]) / ray.dir[i]

            # Ensure T1 is the intersection with the near plane
            if T1 > T2:
                T1, T2 = T2, T1

            # Update Tnear and Tfar
            Tnear = max(T1, Tnear)
            Tfar = min(T2, Tfar)

            if Tnear > Tfar or Tfar < 0:
                return []  # Box is missed or behind the camera

        # Ray intersects with the box
        hit_point = ray.at(Tnear)
        normal = self.compute_normal(hit_point)
        return [Hit(Tnear, normal, self)]

    def compute_normal(self, hit_point):
        # Simple implementation: assumes the box is axis-aligned
        normal = Vec3(0, 0, 0)
        for i in range(3):
            if hit_point[i] == self.params['corner1'][i]:
                normal[i] = -1
            elif hit_point[i] == self.params['corner2'][i]:
                normal[i] = 1
        return normal.normalized()


def test_box():
    box = Box(['corner1', Vec3(0, 0, 0), 'corner2', Vec3(2, 2, 2)])
    print(box)

    ray = Ray(Vec3(1, 1, 1), Vec3(-1, -1, -1).normalized())
    hits = box.intersection(ray)
    for hit in hits:
        print(hit)


def main(args):
    test_box()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

