# Resolution Theorem Prover

In mathematical logic and automated theorem proving, resolution is a rule of inference leading to a refutation theorem-proving technique for sentences in propositional logic and first-order logic. In other words, iteratively applying the resolution rule in a suitable way allows for telling whether a propositional formula is satisfiable and for proving that a first-order formula is unsatisfiable. 


The theorem prover takes a set of first order logic sentences in conjunctive normal form, as input, and tries to prove a set of queries using resolution. This resolution technique uses proof by contradiction and is based on the fact that any sentence in first order logic can be transformed into an equivalent sentence in conjunctive normal form.

* The resolution rule is applied to all possible pairs of clauses that contain complementary literals. After each application of the resolution rule, the resulting sentence is simplified by removing repeated literals. If the sentence contains complementary literals, it is discarded (as a tautology). If not, and if it is not yet present in the clause set S, it is added to S, and is considered for further resolution inferences.
* If after applying a resolution rule the empty clause is derived, the original formula is unsatisfiable (or contradictory), and hence it can be concluded that the initial conjecture follows from the axioms.
* If, on the other hand, the empty clause cannot be derived, and the resolution rule cannot be applied to derive any more new clauses, the conjecture is not a theorem of the original knowledge base.

**Format for input.txt:**


```
  <NQ = NUMBER OF QUERIES>
  <QUERY 1>
    ...
  <QUERY NQ>
  <NS = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE>
  <SENTENCE 1>
    ...
  <SENTENCE NS>
```
  


* Each query will be a single literal of the form Predicate(Constant) or ~Predicate(Constant).
* Variables are all single lowercase letters.
* All predicates (such as Sibling) and constants (such as John) are case-sensitive alphabetical strings that
begin with an uppercase letter.
* Each predicate takes at least one argument. Predicates will take at most 100 arguments. A given
predicate name will not appear with different number of arguments.
  
**Format for output.txt:**


For each query, determine if that query can be inferred from the knowledge base or not, one query per line:
```
  <ANSWER 1>
    ...
  <ANSWER NQ>
```

each answer should be either TRUE if you can prove that the corresponding query sentence is true given the
knowledge base, or FALSE if you cannot.

**Example 1:**

###### input.txt:
```
  6
  F(Joe)
  H(John)
  ~H(Alice)
  ~H(John)
  G(Joe)
  G(Tom)
  14
  ~F(x) | G(x)
  ~G(x) | H(x)
  ~H(x) | F(x)
  ~R(x) | H(x)
  ~A(x) | H(x)
  ~D(x,y) | ~H(y)
  ~B(x,y) | ~C(x,y) | A(x)
  B(John,Alice)
  B(John,Joe)
  ~D(x,y) | ~Q(y) | C(x,y)
  D(John,Alice)
  Q(Joe)
  D(John,Joe)
  R(Tom)
```
###### output.txt:
```
  FALSE
  TRUE
  TRUE
  FALSE
  FALSE
  TRUE
```


**Example 2:**
###### input.txt:
```
  2
  Ancestor(Liz,Billy)
  Ancestor(Liz,Joe)
  6
  Mother(Liz,Charley)
  Father(Charley,Billy)
  ~Mother(x,y) | Parent(x,y)
  ~Father(x,y) | Parent(x,y)
  ~Parent(x,y) | Ancestor(x,y)
  ~Parent(x,y) | ~Ancestor(y,z) | Ancestor(x,z)
```
###### output.txt:
```
  TRUE
  FALSE
```


**Example 3:**
###### input.txt:
```
  1
  Criminal(West)
  6
  ~American(x) | ~Weapon(y) | ~Sells(x,y,z) | ~Enemy(z,America) | Criminal(x)
  Owns(Nono,M1)
  Missile(M1)
  ~Missile(x) | ~Owns(Nono,x) | Sells(West,x,Nono)
  ~Missile(x) | Weapon(x)
  Enemy(Nono,America)
```
###### output.txt:
```
  TRUE
```
