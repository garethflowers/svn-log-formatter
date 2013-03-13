#! /usr/bin/env python
import subprocess
import sys
import argparse
from datetime import datetime

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

def main(argv):
    parser = argparse.ArgumentParser(
        description='Generates a ChangeLog from an SVN Repository.')
    parser.add_argument('url', help='URL of the SVN Repository')
    parser.add_argument('output', help='Location of the Output file')
    args = parser.parse_args()

    query_svn(args.url, args.output)

    sys.exit()

def query_svn(repoUrl, outputFile):
    print ('Connecting to SVN server...')

    try:
        s = subprocess.Popen(['svn', 'log', '--xml', repoUrl],
                              stdout=subprocess.PIPE)
    except:
        print ('Error querying SVN Log')
        sys.exit(1)

    print ('Querying SVN server...')

    out = s.communicate()[0]
    s.stdout.close()

    if s.returncode != 0:
        print ('some error' + str(s.returncode))

    try:
        root = ElementTree.fromstring(out)
    except:
        print ('No results from Repository')
        sys.exit(1)

    f = open(outputFile, 'w+')
    f.write('Revision'.ljust(10))
    f.write('Date'.ljust(10))
    f.write('Author'.ljust(10))
    f.write('Message'.ljust(10))
    f.write('\n')

    for elem in root:
        msgs = elem.find('msg').text

        if not msgs:
            msgs = ''
        elif msgs.startswith('INTERNAL: '):
            continue

        msgs = msgs.encode('utf-8')
        rev = str(elem.attrib.get('revision'))
        author = elem.find('author').text
        date = elem.find('date').text
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        date = datetime.strftime(date, '%d-%m-%y')

        f.write(rev.ljust(10))
        f.write(date.ljust(10))
        f.write(author.ljust(10))
        f.write(msgs)
        f.write('\n')

    f.close()


if __name__ == '__main__':
    main(sys.argv[1:])
