import sys; args=sys.argv[1:]

artists = {}
# format:
# 0: total score
# 1: # of tracks
# 2: dict with key of genre and value of amount of tracks
# 3: highest track
# 4: lowest track

# open tsv
with open(args[0]) as f:
   for line in f:
      data = line.split('\t')
      # important indexes:
      # 0: artist(s)
      # 1: song name
      # 2: genre
      # 9: total score
      # 10: total participants