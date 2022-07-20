import os
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("--12h", help="Use 12h format", action="store_true")
parser.add_argument(
    "--fileprefix", help="Path prefix of sound files", default='')
parser.add_argument('--no-24h-sound', help='Use 0:mm format instead of 24:mm',
                    action='store_true', default=False)
parser.add_argument('--no-half-minute-sound',
                    help='Use 30 minutes instead of half sound', action='store_true', default=False)
parser.add_argument('--disable-no-minutely-sound-error',
                    help='Disable error when no minutely sound', action='store_true', default=False)
args = parser.parse_args()


def checksound(name, type=''):
    if os.path.isfile('../usewav/' + name + type + '.wav'):
        return True
    else:
        return False


def getfile(name, type=''):
    global args
    return args.fileprefix + name + type + '.wav'


def saveList(plist, name):
    with open('../usewav/' + name + '.m3u8', 'w', encoding='utf8') as f:
        for item in plist:
            f.write("%s\n" % item)


start_h = 1
end_h = 24
if args.no_24h_sound:
    start_h = 0
    end_h = 23

for h in range(start_h, end_h + 1):
    files = ['#EXTM3U']

    if checksound(str(h), 'h'):
        files.append(getfile(str(h), 'h'))
    elif (checksound(str(int(h / 10)), 'x') and checksound(str(h % 10), 'h')):
        files.append(getfile(str(int(h / 10)), 'x'))
        files.append(getfile(str(h % 10), 'h'))
    else:
        print('Missing sound: hourly sound: ' + str(h))
        print('Critical Error')
        exit()

    saveList(files, format(h, '0>2') + '00')

    for m in range(1, 61):
        mfiles = files
        if (not(args.no_half_minute_sound) and m == 30 and (checksound('30hlf', 'm'))):
            mfiles.append(getfile('30hlf', 'm'))
        elif (checksound(str(m), 'm')):
            mfiles.append(getfile(str(m), 'm'))
        else:
            if (not(args.disable_no_minutely_sound_error)):
                print('Missing sound: minute sound: ' +
                      str(m) + '; at: hourly sound: ' + str(h))
            continue

        saveList(mfiles, format(h, '0>2') + format(m, '0>2'))
