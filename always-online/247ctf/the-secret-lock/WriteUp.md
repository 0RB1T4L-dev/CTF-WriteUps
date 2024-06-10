## Challenge Name: THE SECRET LOCK

> Category: Reverse Engineering

> Difficulty: Moderate

> Points: 192

Challenge Description:

Can you reverse the secret combination to open the lock and recover the flag?

### Approach

**A HTML File in a Reversing Challenge?**

This challenge only gives us a HTML file, which represents a number lock, where each cell can have a value between 0 and 500. After looking through the file, I finally found the script section with the Javascript to check the code.

```javascript
checkFlag(flag){
    let result = "LOCKED"
	this.dom.lock.classList.remove('verified');
    if (...) { # Constraints, constraints and more constraints
	  result = "";
      for (var idx in flag) {
	    result += (String.fromCharCode(flag[idx]));
	  }
	  this.dom.lock.classList.add('verified');
    }
    return result;
  }
```

There are many constraints which all have to evaluate to true. Sounds like a perfect time to try out z3.

**2. z3 Solver Script**

z3 is a theorem prover from Microsoft Research. I have already seen it in many CTF WriteUps before, but I have never really worked with it, so I thought it would be time to give it a try. Since it was my first time working with z3, I had to spend some time reading documentation and looking at examples. At the end I came up with this Python script.

```python
from z3 import *

s = Solver()

flag = [BitVec('flag{index:d}'.format(index=i), 32) for i in range(40)]
for i in flag:
    s.add(i > 0, i <= 500)

s.add((flag[37] - flag[37]) * flag[15] == 0) 
s.add((flag[3] + flag[31]) ^ (flag[29] + flag[8]) == 234) 
...
s.add((flag[9] - flag[26] + flag[23]) ^ flag[30] == 13)

if s.check() != "unsat": # s.check() == "sat" does not work for some reason
    model = s.model()
    flag_string = ""
    for c in flag:
        flag_string += chr(model.evaluate(c).as_long())
    
    print(flag_string)
```

After the the model is created, the flag is built just like it was in the Javascript code. This way we don't have to enter all values in to the website and can just get the flag.

**3. My Troubles with z3**

While working with z3, ran into the following restrictions:
- If you use Int() in your variable declaration, z3 can not handle bitwise operators like "^" => use BitVectors instead
- For some reason, even when `s.check()` printed "sat", my last if statement always evaluated to false