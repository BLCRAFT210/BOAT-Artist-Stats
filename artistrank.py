import sys; args=sys.argv[1:]
import json

artistdict = {}
# 0: total score
# 1: # of tracks
# 2: dict with key of genre and value of amount of tracks
# 3: highest track
# 4: highest score
# 5: lowest track
# 6: lowest score

with open(args[0]) as f:
   for line in f:
      trackdata = line.split('\t')[1:]
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
#with open('results.json', 'w') as out:
#   json.dump(artistdict, out)

# output as tsv
with open('artistsresult.tsv', 'w') as result:
   # first line
   result.write('Artist\tRating\t# of Tracks\tMain Genre\tHighest Track\tLowest Track\n')

   for artist in artistdict:
      if artistdict[artist][1]>=3:
         # format: artist, rating, track count, main genre, highest track, lowest track
         result.write(artist+'\t'+str((artistdict[artist][0]/artistdict[artist][1]+2)/4)+'\t'+str(artistdict[artist][1])+'\t'+max(artistdict[artist][2], key=artistdict[artist][2].get)+'\t'+artistdict[artist][3]+'\t'+artistdict[artist][5]+'\n')