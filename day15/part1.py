#!/usr/local/bin/python3

sensors = [
  (1518415, 2163633),(2474609, 3598166),(426959,  473371 ),(3999598, 1984775),
  (2459256, 2951561),(2925882, 2862933),(3539174, 3882566),(3044887, 3798155),
  (1792818, 3506985),(3761945, 3304667),(71968,   3823892),(2902345, 3999748),
  (2074989, 2347435),(1115220, 1782338),(369130,  2348958),(2525090, 1917940),
  (2861163, 3386968),(3995081, 2010596),(3038274, 534921 ),(3646366, 2868267),
  (3308360, 1653497),(1996072, 995783 ),(3852158, 950900 ),(3061849, 2428914),
  (2788254, 3983003),(694411,  1882565),(2647250, 2551966),(1079431, 3166226),
  (3929172, 2196495),(3883296, 2487406),(1271911, 1529880),
]

beacons = [
  (1111304,  1535696),(2691247,  4007257),(-529106,  1145419),(3975468,  2000000),
  (2132806,  2866452),(3325001,  3024589),(3132375,  3541509),(3132375,  3541509),
  (2132806,  2866452),(3325001,  3024589),(-1085197, 3401157),(2691247,  4007257),
  (2132806,  2866452),(1111304,  1535696),(1111304,  1535696),(2603675,  2276026),
  (3132375,  3541509),(3975468,  2000000),(4354209,  -17303),(3325001,  3024589),
  (3975468,  2000000),(1111304,  1535696),(3975468,  2000000),(2603675,  2276026),
  (2691247,  4007257),(1111304,  1535696),(2603675,  2276026),(2132806,  2866452),
  (3975468,  2000000),(3975468,  2000000),(1111304,  1535696)
]

sensors_t = [
  (2,  18),(9,  16),(13, 2 ),(12, 14),(10, 20),(14, 17),(8,  7 ),(2,  0 ),(0,  11),
  (20, 14),(17, 20),(16, 7 ),(14, 3 ),(20, 1 ),
]

beacons_t = [
  (-2, 15),(10, 16),(15, 3),(10, 16),(10, 16),(10, 16),(2,  10),(2,  10),(2,  10),
  (25, 17),(21, 22),(15, 3),(15, 3),(15, 3),
]

class Grid(object):
  def __init__(self):
    self.nearest_beacon_by_sensor = {}

  def get_beacons(self):
    return set(self.nearest_beacon_by_sensor.values())

  def get_sensors(self):
    return set(self.nearest_beacon_by_sensor.keys())

  def get_all_points(self):
    return self.get_beacons().union(self.get_sensors())

  def get_closest_beacon(self, pt):
    return min(self.get_beacons(), key = lambda x: Grid.distance(x, pt))

  def get_closest_sensor(self, pt):
    return min(self.get_sensors(), key = lambda x: Grid.distance(x, pt))

  def get_min_x(self):
    return min([b[0] for b in self.get_all_points()])

  def get_max_x(self):
    return max([b[0] for b in self.get_all_points()])

  def get_min_y(self):
    return min([b[1] for b in self.get_all_points()])

  def get_max_y(self):
    return max([b[1] for b in self.get_all_points()])

  def is_excluded(self, pt):
    for s in self.get_sensors():
      exclusion_range = Grid.distance(s, self.nearest_beacon_by_sensor[s])
      if Grid.distance(pt, s) <= exclusion_range:
        return True
    return False

  def distance(p1, p2):
    return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])


# construct grid    
LINE_OF_INTEREST = 2000000
g = Grid()
for b, s in zip(beacons, sensors):
  g.nearest_beacon_by_sensor[s] = b

count = 0
for x in range(g.get_min_x(), g.get_max_x() + 1):
  here = (x, LINE_OF_INTEREST)
  if not here in g.get_beacons() and g.is_excluded(here):
    count += 1
print(count)
