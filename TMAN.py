import sys

from dynamic_ring import DynamicRing
from ring import Ring

args = sys.argv
N = int(args[1])
k = int(args[2])
topology = args[3]

if topology == 'R':
    ring = Ring(N, k, 40)
elif topology == 'D':
    radii = [int(r) for r in args[4:]]
    dynamic_ring = DynamicRing(N, k, len(radii), radii)
else:
    print("Unknown Topology")
