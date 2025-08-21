## Distrib Explanation

The source code `flag_checker.c` was compiled with some compiler options (which I forgot), but the key option was:<br>
    `gcc -o flag_checker flag_checker.c -ffreestanding -nostdlib -static -s -O1 -T minimal.ld`
in particular, the last option `-T minimal.ld`

`minimal.ld` is a linker script that removes alot of (probably important) stuff, which is why the binary cannot run. But it still retains enough information to decompile and figure out the flag.

## Solve Method

Usually you might be able to use symbolic execution (like angr) to solve the flag character, but I intentionally included some weird branchless constructs (eg Line B) that cannot be easily resolved:

```c
  if ((int)*(char *)(flag + 18) ==                                           // Line A
      (-(uint)(*(char *)(flag + 5) == DAT_00400585) & (int)DAT_00400586)) {  // Line B
    uVar1 = FUN_0040039b();             // Our target
  }
  // DAT_00400585 -> 'f'
  // DAT_00400586 -> 'L'
```

There are technically alot of solutions to this if you consider null character (0x00), but only one actual solution. 

In this case, if `flag[5] == 'f'` then 
```c
-(uint)(*(char *)(flag + 5) == DAT_00400585)  // Line B
// will become
-(uint)(true)
// or equivalently
-(1)
// which is 0xFFFFFFFFF in 2comp, i.e. all bits set

// so the whole condition
(int)*(char *)(flag + 18) ==                                              // Line A
      (-(uint)(*(char *)(flag + 5) == DAT_00400585) & (int)DAT_00400586)  // Line B
// becomes
(int)*(char *)(flag + 18) == DAT_00400586
// which implies
flag[18] == 'L'
```

So you can get the charactes for `flag[5] = 'f'` and `flag[18] = 'L'`.

Other functions are easier, performing only simple arithmetic operations:

```c
  if (((int)*(char *)(param_1 + 10) - 0x13U ^ 0x2b) + 10 == (int)DAT_00400587) {
    uVar1 = FUN_00400362();
  }
```

## Alternative (llm)

Or you can throw each function into an llm to solve:
[Flag Checker Sample Solve](https://g.co/gemini/share/b1b78632e6f9)

## Extra

Source Code: `flag_checker.c`<br>
Runnable Binary: `flag_checker_clean`<br>
Linker Script: `minimal.ld`<br>
Original Distrib: `flag_checker`