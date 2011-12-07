Ever want to know what the hell that python script is doing?  Enter the
Inspect Shell.

How to set up
=============

Put inspect_shell.py in the directory of the script you want to inspect.

Add

```python
import inspect_shell
```

to the top of that script.

That's it.

How to use
==========

Run your script.  Then run:

    $ python inspect_shell.py
    
You'll now have an interactive shell to your script.  Anything you do will
affect the script *on the fly.*