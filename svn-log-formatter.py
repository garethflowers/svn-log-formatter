import subprocess
import sys
from datetime import datetime

try:
  import xml.etree.cElementTree as ElementTree
except ImportError:
  import xml.etree.ElementTree


def init():
  if sys.argv[1] == '':
    print ('error')
  else:
    print ('ok')


def query_svn():
  print (sys.argv[1])
  print ('Connecting to SVN server...')

  try:
    s = subprocess.Popen( ['svn', 'log', '--xml', 'https://casper:8443/svn/crm/trunk/'], stdout = subprocess.PIPE )
  except:
    print ("Error querying SVN Log")
    sys.exit(1)

  print ('Querying SVN server...')

  out, err = s.communicate()

  root = ElementTree.fromstring(out)

  f = open('workfile.txt', 'w+')

  for elem in root:
    rev = str(elem.attrib.get('revision'))
    author = elem.find('author').text
    msgs = elem.find('msg').text
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
  query_svn()
  sys.exit(0)
