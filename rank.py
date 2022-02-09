import sys; args=sys.argv[1:]
import json

artistdict = {}
# format:
# 0: total score
# 1: # of tracks
# 2: dict with key of genre and value of amount of tracks
# 3: highest track
# 4: highest score
# 5: lowest track
# 6: lowest score

# open tsv
with open(args[0]) as f:
   # parse each track line by line
   for line in f:
      trackdata = line.split('\t')
      # important indexes:
      # 0: artist(s)
      # 1: song name
      # 2: genre
      # 9: total score
      # 10: total participants

      # run stats for each artist in the track
      for artist in trackdata[0].split(', '):
         trackscore = int(trackdata[9])/int(trackdata[10])
         
         # create key in dict if it doesn't exist
         if artist not in artistdict:
            artistdict[artist] = [0,0,{},'',-3,'',3]
         
         # update total score
         artistdict[artist][0] += trackscore
         # update track count
         artistdict[artist][1] += 1

         # create genre for artist if it doesn't exist
         if trackdata[2] not in artistdict[artist][2]:
            artistdict[artist][2][trackdata[2]] = 0
         # update genre count
         artistdict[artist][2][trackdata[2]] += 1

         # update highest track
         if trackscore>artistdict[artist][4]:
            artistdict[artist][3] = trackdata[1]
            artistdict[artist][4] = trackscore

         # update lowest track
         if trackscore<artistdict[artist][6]:
            artistdict[artist][5] = trackdata[1]
            artistdict[artist][6] = trackscore

# test print
with open('results.json', 'w') as out:
   json.dump(artistdict, out)