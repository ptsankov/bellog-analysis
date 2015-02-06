from rule import Rule
import sys
import getopt

vars = {'X', 'Y', 'Z'}
bools = {}

def main():
    preds = set()
    filenameFPL = None
    outputFile = None
    n = None
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:n:', ['input'])
    for o, a in opts:
        if o == '-i':
            filenameFPL = a
        if o == '-o':
            outputFile = a
        if o == '-n':
            n = int(a)

    if filenameFPL is None or outputFile is None or n is None:
        print 'Usage: python', sys.argv[0], '-i <FPL input filename> -o <output file> -n <domain size>'
        sys.exit()
    
    domain = {'a' + str(x) for x in range(0,n)}
    # convert to basic rules
    fileFPL = open(filenameFPL)        
    rules = set()
    groundRules = set()
    for line in fileFPL:
        tmpRules = None
        if '[' in line:
            # composite rule
            tmpRules = Rule.fromCompositeString(line.rstrip())
        else:
            # basic rule
            tmpRules = [Rule.fromString(line.rstrip())]
        for r in tmpRules:
            if r.isGround():
                groundRules.add(r)
            else:
                rules.add(r)
    fileFPL.close()
    
    while len(rules) > 0:
        rule = rules.pop()
        var = rule.vars().pop()
        for const in domain:
            newRule = rule.getCopy()
            newRule.replaceArg(var, const)
            if newRule.isGround():
                groundRules.add(newRule)
            else:
                rules.add(newRule)
                
                
    atoms = set()
    implications = []
    for rule in groundRules:
        atoms.add(rule.head.getProposition())
        body = []
        for literal in rule.body:
            atoms.add(literal.atom.getProposition())
            if literal.op is None or literal.op == '#':
                body.append(literal.atom.getProposition() + '_t')
            elif literal.op == '!':
                body.append('(not ' + literal.atom.getProposition() + '_e)')
            else:
                print 'you are wrong'
                sys.exit(-1)
        implications.append( (' '.join(body), rule.head.getProposition()+ '_t') )
        body = []
        for literal in rule.body:
            atoms.add(literal.atom.getProposition())
            if literal.op is None:
                body.append(literal.atom.getProposition() + '_e')
            elif literal.op == '#':
                body.append(literal.atom.getProposition() + '_t')
            elif literal.op == '!':
                body.append('(not ' + literal.atom.getProposition() + '_t)')
            else:
                print 'you are wrong'
                sys.exit(-1)
        implications.append( (' '.join(body), rule.head.getProposition()+ '_e') )                       
    
    sortedImplications = {}
    heads = set([x for (y,x) in implications])
    for head in heads:
        sortedImplications[head] = []
    for (body, head) in implications: 
        sortedImplications[head].append(body)    
    
    out = open(outputFile, 'w')
    for atom in atoms:
        out.write('(declare-const ' + atom +'_t ' + 'Bool)\n')
        out.write('(declare-const ' + atom +'_e ' + 'Bool)\n')
    for atom in atoms:
        out.write('(assert (=> ' + atom +'_t ' +  atom + '_e))\n')
    for head in heads:
        disjBodies = '(or '
        for body in sortedImplications[head]:
            disjBodies += '(and ' + body + ') '
        disjBodies += ')'
        out.write('(assert (=> ' + disjBodies + ' '+ head + '))\n')
        out.write('(assert (=> ' + head + ' ' + disjBodies + '))\n')
    out.write('(assert (not check_m_t))\n')
    out.write('(check-sat)\n')
    out.write('(get-model)\n')
    
if __name__ == '__main__':
    main()
