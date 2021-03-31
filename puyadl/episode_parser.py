def parseEpisodeFilter(episodes):
    filterList = episodes.split(',')
    allowedEps = []
    # Two types of filters are allowed:
    # range (x-y) i.e. 1-3
    # single number i.e. 2
    for f in filterList:
        try:
            fInt = int(f)
            allowedEps.append(fInt)
        except:
            if "-" in f:
                ranges = f.split('-')
                if len(ranges) == 2:
                    x = int(ranges[0])
                    y = int(ranges[1])
                    if x == y:
                        allowedEps.append(x)
                    elif y > x:
                        for i in range(x, y+1):
                            allowedEps.append(i)
                    else:
                        print("This program is too dumb to interpret this")
                else:
                    print(f, "is invalid episode filter")
            else:
                print(f, "is invalid episode filter")
    return allowedEps