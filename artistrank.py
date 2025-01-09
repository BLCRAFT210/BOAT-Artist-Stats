import re
import sys
args = sys.argv[1:]

SCALING_FACTOR = 0.8

artistdict = {}

with open(args[0]) as f:
    for line in f:
        trackdata = line.split('\t')[1:]
        # important indexes:
        # 0: artist(s)
        # 1: song name
        # 2: genre
        # 3: release date
        # 11: raw score

        artists = []
        remixerSearch = re.search(r'[^\(]+(?= Remix\))', trackdata[1])
        if (remixerSearch == None):
            artists = trackdata[0].split(' | ')
        else:
            artists = remixerSearch.group().split(' & ')

        # run stats for each artist in the track
        for artist in artists:
            trackscore = float(trackdata[11])
            release_date = trackdata[3]

            # create key in dict if it doesn't exist
            if artist not in artistdict:
                artistdict[artist] = [0, 0, {}, '', -3,
                                      '', 3, '9999-99-99', '0000-00-00', []]

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
            if trackscore > artistdict[artist][4]:
                artistdict[artist][3] = trackdata[1]
                artistdict[artist][4] = trackscore

            # update lowest track
            if trackscore < artistdict[artist][6]:
                artistdict[artist][5] = trackdata[1]
                artistdict[artist][6] = trackscore

            # update debut date
            if release_date < artistdict[artist][7]:
                artistdict[artist][7] = release_date

            # update recent date
            if release_date > artistdict[artist][8]:
                artistdict[artist][8] = release_date

            # add track score to list for score calculation
            artistdict[artist][9].append(trackscore)

# calculate normalized scores and store them in a list
artist_scores = []
for artist in artistdict:
    if artistdict[artist][1] >= 3:
        sorted_scores = sorted(artistdict[artist][9], reverse=True)
        weighted_score = sum(score * (SCALING_FACTOR ** i)
                             for i, score in enumerate(sorted_scores))
        geometric_sum = sum(
            SCALING_FACTOR ** i for i in range(artistdict[artist][1]))
        normalized_score = weighted_score / geometric_sum
        artist_scores.append((artist, artistdict[artist], normalized_score))

# sort by normalized score descending
artist_scores.sort(key=lambda x: x[2], reverse=True)

# output as tsv
with open('artistsresult.tsv', 'w') as result:
    # first line
    result.write(
        'Artist\t# of Tracks\tMain Genre\tDebut\tRecent\tHighest Track\tLowest Track\tScore\n')

    for artist, data, normalized_score in artist_scores:
        result.write(
            artist + '\t' +
            str(data[1]) + '\t' +
            max(data[2], key=data[2].get) + '\t' +
            data[7] + '\t' +
            data[8] + '\t' +
            data[3] + '\t' +
            data[5] + '\t' +
            str(normalized_score) + '\n'
        )
