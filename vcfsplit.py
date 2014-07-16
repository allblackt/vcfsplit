#!/usr/bin/env python
import argparse
import os.path
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help='Input VCF file')
    parser.add_argument("destination", nargs='?', default='./',
                        help='Where to dump the resulting .vcf files')
    args = parser.parse_args()
    fname = args.file
    destination = args.destination

    if not os.path.isfile(fname):
        print fname, 'does not exist!'
        exit(1)

    with open(fname) as f:
        card = ''
        dump_name = ''
        contacts_read = 0;
        for line in f:
            line = line.replace('\r\n','').replace('\n','').strip()
            card = card + line + '\n'
            if line == 'END:VCARD':
                dump_card(card, dump_name, destination)
                card = ''
                contacts_read += 1
                print contacts_read, 'contacts read...'
            elif line.startswith('FN:'):
                dump_name = re.sub(r'[^\w\-\.&\s]', '', line[2:]).strip()
                dump_name = dump_name.replace(' ', '_')

def dump_card(card, dump_name, destination = ''):
    if not len(dump_name.strip()):
        return
    try:
        save_path = os.path.join(destination, dump_name + '.vcf')
        with open(save_path, 'w') as f:
            f.write(card)
    except Exception, e:
        print 'Error occured while writing', dump_name
        print e



if __name__ == '__main__':
    main()
