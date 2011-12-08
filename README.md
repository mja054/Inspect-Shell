Ever want to know what the hell that python script is doing?  Enter the
Inspect Shell.  Inspect Shell lets you print/alter globals and run functions
without interrupting the running script.

Inspect Shell is not a pdb-style debugger.

How to set up
=============

Put inspect_shell.py in the directory of the script you want to inspect.

Add

```python
import inspect_shell
```

to the top of that script.

**That's it.**

How to use
==========

Run your script.  Then run:

    $ python inspect_shell.py
    
You'll now have an interactive shell to your script.  Anything you do will
affect the script **on the fly.**  Be careful :)

Example
=======
    $ rs:1234> print some_module
    <module 'some_module' from '/whatever'>

    $ rs:1234> print some_module.some_config_value
    492

    $ rs:1234> some_module.some_config_value = 292

...And your script keeps on running, but with whatever changes you made from the shell.


Be Careful
==========

Inspect Shell provides *no locking* when you're altering the global and local namespace.  You may experience undefined behavior if you do much more than passively examine objects.
