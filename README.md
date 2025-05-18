# Proving Analyticity of Partial Valuations

This repository contains a
[Maude](https://maude.cs.illinois.edu/wiki/The_Maude_System) specification to
assist in proving correct the criteria for extending partial valuations.

The approach is as follows:

1. A **partial model** is computed by non-deterministically assigning values to formulas:
   - *A* (in the case of extending the valuation with `Box A`
   - *A* and *B* (in the case of extending the valuation with `Imp A B`
   
   To analyze each connective, an additional formula *C* is introduced. This
   column tests whether, when the model is extended, the supporting rows for
   *C* remain valid. 

2. The column corresponding to the newly introduced `BOX` or `IMP` formula is
   completed by deterministically assigning it a value.

3. The generated extension is then checked to ensure that:
   - the relational conditions are satisfied, and
   - all values are properly supported.

## Main Files

- `base.maude`: Contains the basic definitions for truth values, rows, matrices, etc.
- `analyticity.maude`: Defines the rewrite rules required for the analysis.
- One file per modal logic family (e.g., `KT4.maude`).

## Querying the System

The analysis is performed using Maude's strategy language. For example, in
`KT4.maude`, the following command checks the first extension case of `BOX`:

```maude
dsrew in CHECK-ANALITICITY-BOX1 : initBox using 
   guess ! ; depC ; depA ; guess ! ; 
   value ! ; guess ! ; ignore ; 
   (match no-case ? fail : idle) ; one(simplify) ! ; check .
```

The strategy used by the command `dsrew` can be explained as follows: 

- `guess !`: non-deterministically assigns values to *A* and *C*.
- `depC ; depA`: Generates dependencies due to *C* and *A* (in case the values assigned requires a support).
- `guess !`: Guess the values in the rows created by the previous strategy 
- `value !`:  Deterministically assigns a value to the new BOX formula.
- `ignore ; (match ...)`: Skips cases that don't match the intended scenario.
- `one(simplify)`: Removes duplicated or redundant cases.
- `check`: Verifies that all relational and support conditions hold.

Here an example: 

```
$> maude KT4
...
Maude> dsrew in CHECK-ANALITICITY-BOX1 : initBox using 
    guess ! ; depC ; depA ; guess ! ; 
    value ! ; guess ! ; ignore ; 
    (match no-case ? fail : idle) ; one(simplify) ! ; check .

Solution 1
rewrites: 186 in 0ms cpu (0ms real)
result OKState: ok((
[A : t, C : T, NEW : F]: 1, 
[A : F, C : T, NEW : F]: (2 <- 1)))

...

Solution 142
rewrites: 13630 in 10ms cpu (11ms real)
result OKState: ok((
[A : t, C : f, NEW : F]: (2 <- 1), 
[A : f, C : t, NEW : F]: (2 <- 1), 
[A : f, C : f, NEW : F]: 1))

No more solutions.
rewrites: 14093 in 11ms cpu (12ms real)
```

In logics with more complex cases, you can simply check that no result leads to
failure by verifying that the final result does not belong to the sort `FState`
(failing state):

```
Maude> dsrew in CHECK-ANALITICITY-BOX1 : initBox using 
   guess ! ; depC ; depA ; guess ! ; 
   value ! ; guess ! ; ignore ; 
   (match no-case ? fail : idle) ; one(simplify) ! ; check ;
   match FAIL:FState .

No solution.
rewrites: 14093 in 8ms cpu (8ms real)
```
