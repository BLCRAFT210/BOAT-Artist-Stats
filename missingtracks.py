import sys; args=sys.argv[1:]

boattracks = set()
infotracks = set()

with open(args[0]) as f:
   for line in f:
      trackdata = line.split('\t')
      boattracks.add(trackdata[2].lower().strip())

with open(args[1]) as f:
   for line in f:
      trackdata = line.split('\t')
      infotracks.add(trackdata[6].lower().strip())

# symmetric difference
print(boattracks ^ infotracks)