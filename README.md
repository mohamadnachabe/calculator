Python Calculator 
======

Evaluates mathematical expressions as strings.

## Example:

```python
  from calculator.calculator import evaluate
  
  t = evaluate('(4 + 4) * 344 + (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)')
```

evaluate_o is a more optimized version of evaluate. It avoids the usage of python's splitting operation in the recursive calls. 
```python
  from calculator.calculator_o import evaluate_o
  
  t = evaluate_o('(4 + 4) * 344 + (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)')
```

## Supported operations:

|Operation|Symbol|
|:---:|:---:|
|Addition|+|
|Subtraction|-|
|Multiplication|*|
|Division|/|
|Exponentiation|^|
|Grouping|( )|
