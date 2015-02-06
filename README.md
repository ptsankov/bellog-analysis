I. DESCRIPTION

This is a framework for formulating policy analysis questions for
policies written in FPL.

II. INSTALL

To use the framework you need to install the following software:
- Microsoft's Z3 Solver
  See http://z3.codeplex.com/
- Python 2.6+
  See  http://python.org/


III. USING THE FRAMEWORK

The analysis questions must be encoded as query validity FPL
questions. At this point the analysis framework lacks a tool for
translating containment problems into query validity. One can however
manually follow the reduction steps given in the extended version of
the paper, which can be downloaded at
www.infsec.ethz.ch/research/software/fpl/fpl-ext.pdf.

Example analysis questions are found in the folder called "questions".
Below we show how the analysis questions given in the paper are
answered with the analysis framework. 

A. Policy 3 and Fail-safety Requirement 1

Copy the template of the analysis question:
```cp questions/pol3_fr1_template.fpl tmp.fpl```

Instantiate the template for a given domain of constants. E.g., to
instantiate for 10 constants:
```python code/qval_to_smt2.py -i tmp.fpl -o tmp.z3 -n 10```

Run the resulting file tmp.z3 with Z3:
```z3 -smt2 tmp.z3```

The output of Z3 should be "unsat", i.e. Z3 could not find a
counter-example where the analysis question is answered negatively.

B. Policy 5 and Fail-safety Requirement 2
```
cp questions/pol5_fr2_template.fpl tmp.fpl
python code/qval_to_smt2.py -i tmp.fpl -o tmp.z3 -n 10
z3 -smt2 tmp.z3
```

C. Policy 2 and Fail-safety requirement 3

For the first question:
```cp questions/pol2_fr3_direct_template.fpl tmp.fpl```
To verify policy 2 there is an extra step that expands all possible
delegation chains:
```
python code/pol2_fr3.py -o tmp.fpl -n 5
python code/qval_to_smt2.py -i tmp.fpl -o tmp.z3 -n 5
z3 -smt2 tmp.z3
```

The verification of the second question is similar.

D. Policy6 and Fail-safety Requirement 2

For the first question:
```
cp questions/pol6_fr3_direct_template.fpl tmp.fpl
python code/pol6_fr3.py -n 5 -o tmp.fpl
python code/qval_to_smt2.py -i tmp.fpl -o tmp.z3 -n 5
z3 -smt2 tmp.z3
```

The verification of the second question is similar.
