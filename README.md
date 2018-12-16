# quine-mccluskey

This program takes a sum of products (SOP) of 4 variables as input, and returns the *minimized expression* through the Quine-McCluskey method. It shows the number of literals in the final solution, too.

## 1. How to Execute:
`$ python quine-mc.py`

## 2. Example:
input: (!A!B!C!D + !A!B!CD + !A!BC!D +!AB!CD + !ABC!D + !ABCD + A!B!C!D + A!B!CD +A!BC!D + ABC!D)
output: (!B!C + C!D + !ABD) - 7 literals.

### References:
**Quine-McCluskey.** Available at: [https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm)

**Petrick's Method** Available at: [https://en.wikipedia.org/wiki/Petrick%27s_method](https://en.wikipedia.org/wiki/Petrick%27s_method)
