


# command delimeter for the serial communication to arduino
MAGIC = 200

def clip(x, minval, maxval):
    if x > maxval:
        return maxval
    elif x < minval:
        return minval
    else:
        return x

def clip_servos(servos):
    return [clip(s, 0, 180) for s in servos]

