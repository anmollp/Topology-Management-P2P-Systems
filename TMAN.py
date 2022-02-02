import sys
import os

from dynamic_ring import DynamicRing
from ring import Ring

args = sys.argv
N = int(args[1])
k = int(args[2])
topology = args[3]

home = os.path.expanduser("~")
homework_directory = 'Patil_EEL6761_HW1'

if not os.path.exists(os.path.join(home, homework_directory)):
    os.mkdir(os.path.join(home, homework_directory))

if topology == 'R':
    ring = Ring(N, k, 40)
elif topology == 'D':
    radii = [int(r) for r in args[4:]]
    dynamic_ring = DynamicRing(N, k, len(radii), radii)
else:
    print("Unknown Topology")
