import sys; args=sys.argv[1:]

boattracks = set()
infotracks = set()

# turns each row into artist|track|genre

with open(args[0]) as f:
   for line in f:
      trackdata = line.split('\t')
      boattracks.add(trackdata[1]+'|'+trackdata[2]+'|'+trackdata[3])

with open(args[1]) as f:
   for line in f:
      trackdata = line.split('\t')
      infotracks.add(trackdata[5]+'|'+trackdata[6]+'|'+trackdata[4])

# symmetric difference
print(boattracks ^ infotracks)