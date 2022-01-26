---
title: "Valid Number - By DFA"
tags:
    - computer science
    - algorithm
    - leetcode
    - C++
mathjax: true
date: "2016-11-27"
slug: "valid-number"
---

## Introduction to the Problem

The question asks the programmer to validate whether a string is a valid representation of a number. After some trials, we find that the question accepts a few formats:

1. pure integer
2. real number (decimal representation), including omitted zero, for example ".5", "12."
3. scientific number, that looks like "{Real Number}e{Integer}"
4. integer and real number can be signed
5. ignore any surrounding white spaces

In order to solve the problem in linear time, most solutions set a few flags. This is simple, and quite efficient in both time and space. In fact, I don't really consider this problem qualified for _hard_.

Just to add some fun, this problem can be solved using a very textbook DFA. The code is elegant, less space efficient (but only for a constant amount) than the flag algorithm. In fact, the latter is just a compact, specialized DFA in essence. The trade-off is more variables and branching.

## The Algorithm

The first step, we trim the string. There is probably not efficient in bringing white space processing into the DFA.


```cpp
static inline string trim(string s)
{
    if (s.size() == 0) return s;

    char *c = &(s[0]), // starting pointer
         *d = c + s.length() - 1; // ending pointer

    while (*c != '\0' && isspace(*c)) c++;
    while (d != c && isspace(*d)) d--;

    *(d + 1) = '\0';

    return string(c);
}
```

### DFA - States

Any accepted string can be divided into a few parts:

1. before decimal, the left part of a real number
2. decimal
3. after decimal, the right part of a real number
4. e character
5. the exponent, the right to 'e'

Any part could potentially empty. The (1) and (5) could potentially be preceded with a sign ('+' or '-').

Then, we can collect all states based on the grammar:

| state | meaning|
|------|--------|
|`START` | starting state |
|`REALLEFT` | before encountering any decimal |
|`DOT` | encounter a regular decimal |
|`E` | encounter an 'e'|
|`REALRIGHT` | have encountered a decimal|
|`DOT_E` | have encountered a decimal whose left is omitted|
|`ERIGHT` | have encountered 'e', and is therefore part of the exponent|
|`SIGN1` | the sign on the left of the 'e'|
|`SIGN2` | the sign on the right of the 'e'|
|`FAULT` | the faulty state |

The starting state is `START`.

`FAULT` is a special state, that the DFA will halt whenever it meets `FAULT`, so that we do not have to process the rest of the string.

### DFA - Transition

The transition function is a matrix that maps (state, input char) to state.

$$
\begin{blockarray}{cccccc}
a & b & c & d & e \\
\begin{block}{(ccccc)c}
  1 & 1 & 1 & 1 & 1 & f \\
  0 & 1 & 0 & 0 & 1 & g \\
  0 & 0 & 1 & 0 & 1 & h \\
  0 & 0 & 0 & 1 & 1 & i \\
  0 & 0 & 0 & 0 & 1 & j \\
\end{block}
\end{blockarray}
$$

| _states_  | DIGIT     | SIGN  | DOT   | E     | NDIGIT |
|-----------|-----------|-------|-------|-------|--------|
| START     | REALLEFT  | SIGN1 | DOT_E | FAULT | FAULT  |
| REALLEFT  | REALLEFT  | FAULT | DOT   | E     | FAULT  |
| DOT       | REALRIGHT | FAULT | FAULT | E     | FAULT  |
| E         | ERIGHT    | SIGN2 | FAULT | FAULT | FAULT  |
| REALRIGHT | REALRIGHT | FAULT | FAULT | E     | FAULT  |
| DOT_E     | REALRIGHT | FAULT | FAULT | FAULT | FAULT  |
| ERIGHT    | ERIGHT    | FAULT | FAULT | FAULT | FAULT  |
| SIGN1     | REALLEFT  | FAULT | DOT_E | FAULT | FAULT  |
| SIGN2     | ERIGHT    | FAULT | FAULT | FAULT | FAULT  |

![grammar](/images/valid_number_dfa.svg)

### DFA - Termination

The DFA will terminate when

- input is depleted
- state is `FAULT`

The string will be accepted if the termination state is one of following:

- `REALLEFT`
- `REALRIGHT`
- `ERIGHT`
- `DOT`

In all other cases, the format is somewhat faulty. For example, if the DFA ended at `E`, then the string looks like `"{some number}e"`, which is not acceptable.

---

The running of the DFA is easy. Simply iterate over the input, and let the transition matrix do its magic.



## Complete Code:

```cpp
class Solution {

    static inline string trim(string s)
    {
        if (s.size() == 0) return s;

        char *c = &(s[0]),
             *d = c + s.length() - 1;
        while (*c != '\0' && isspace(*c))
            c++;

        while (d != c && isspace(*d))
            d--;

        *(d + 1) = '\0';

        return string(c);
    }

    int START = 0;
    int REALLEFT = 1;
    int DOT = 2;
    int E = 3;
    int REALRIGHT = 4;
    int DOT_E = 5;
    int ERIGHT = 6;
    int SIGN1 = 7;
    int SIGN2 = 8;
    int FAULT = -1;

    int DIGIT = 0;
    int NDIGIT = 4;
    int SIGN = 1;

    int G[45] =
    {//  DIGIT       SIGN    DOT      E     NDIGIT
        REALLEFT,   SIGN1,  DOT_E,  FAULT,  FAULT,
        REALLEFT,   FAULT,  DOT,    E,      FAULT,
        REALRIGHT,  FAULT,  FAULT,  E,      FAULT,
        ERIGHT,     SIGN2,  FAULT,  FAULT,  FAULT,
        REALRIGHT,  FAULT,  FAULT,  E,      FAULT,
        REALRIGHT,  FAULT,  FAULT,  FAULT,  FAULT,
        ERIGHT,     FAULT,  FAULT,  FAULT,  FAULT,
        REALLEFT,   FAULT,  DOT_E,  FAULT,  FAULT,
        ERIGHT,     FAULT,  FAULT,  FAULT,  FAULT
    };

public:
    bool isNumber(string s) {
        s = trim(s);

        if (s.size() == 0) return false;

        char prev = '\0';
        int state = START;

        for (auto c : s)
        {
            if (state == FAULT) return false;

            int ch = (isdigit(c)) ? DIGIT
                    : (c == '.')  ? DOT
                    : (c == 'e')  ? E
                    : (c == '+')  ? SIGN
                    : (c == '-')  ? SIGN
                    : NDIGIT;

            state = G[state * 5 + ch];
        }

        if (state == E || state == DOT_E || state == SIGN1 || state == SIGN2 || state == START || state == FAULT)
            return false;
        return true;
    }
};
```