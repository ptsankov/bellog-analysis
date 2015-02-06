import itertools
import sys
import getopt


def main():
  domainSize = None
  outputFilename = None
  opts, args = getopt.getopt(sys.argv[1:], 'n:o:', ['input'])
  for o, a in opts:
    if o == '-n':
      domainSize = int(a)
    if o == '-o':
      outputFilename = a

  if domainSize is None or outputFilename is None:
    print 'Usage: python', sys.argv[0], '-n <domain size> -o <output file (fpl)>'
    sys.exit()

  outputFile = open(outputFilename, 'a')

  for chain in itertools.permutations(['a' + str(x) for x in range(0,domainSize)]):
    for length in range(1, len(chain)):
      delegation = chain[0:length+1]
      rule1 = 'chain(' + delegation[-1] + ') :- ownerTF(' + chain[0] + ')'
      rule2 = 'pol2(' + delegation[-1] + ') :- ownerTF(' + chain[0] + ')'
      for cur in range(0, len(delegation)-1):
        rule1 += ' ^ give(' + delegation[cur] + ',' + delegation[cur+1] + ')'
        rule2 += ' ^ valid(' + delegation[cur] + ',' + delegation[cur+1] + ')'
      outputFile.write(rule1)
      outputFile.write('\n')
      outputFile.write(rule2)
      outputFile.write('\n')

  outputFile.close()
  
if __name__ == '__main__':
  main()
