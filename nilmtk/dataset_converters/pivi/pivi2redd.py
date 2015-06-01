import json
import sys
import ConfigParser
import os

try:
    input_file = sys.argv[1]
    config_file = sys.argv[2]
    output_dir = sys.argv[3]
except IndexError:
    print 'Usage: {} <in file> <config> <out dir>'.format(sys.argv[0])


conf = ConfigParser.ConfigParser()
conf.readfp(open(config_file))

houses = conf.items('houses')
circuits = dict(conf.items('circuits'))

out_files = {}


def create_dirs():
    for house in houses:
        house_dir = os.path.join(output_dir, 'house_'+str(house[0]))
        if not os.path.exists(house_dir):
            os.makedirs(house_dir)
        out_files[int(house[0])] = {}


def create_files(mode='w'):
    for circuit, h in circuits.iteritems():
        h, m = get_house_meter(circuit)
        house_dir = os.path.join(output_dir, 'house_'+str(h))
        file_name = os.path.join(house_dir, 'channel_'+str(m)+'.dat')
        out_files[int(h)][m] = open(file_name, mode)
        print 'Circuit {}, house {}, meter {}, file {}'.format(circuit, h, m, file_name)


def get_house_meter(circuit_id):
    h = circuits[str(circuit_id)]
    meter = 10 * ((int(circuit_id) - 9000) / 10)
    meter += (int(circuit_id) - 9000) % 10
    return h, meter

# Create the directory structure
create_dirs()
create_files()

print 'Writing values ...'
with open(input_file, 'r') as data:
    for line in data:
        m = json.loads(line)
        house, meter = get_house_meter(m['circuit'])
        time = m['collector_timestamp'] / 1000
        power = m['proc']['power']
        out = " ".join((str(time), str(power)))
        out_files[int(house)][meter].write(out + '\n')

print 'Closing files...'
for b, m in out_files.iteritems():
    for meter in m.values():
        meter.close()
