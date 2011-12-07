Ever want to know what the hell that python process is doing?  Enter the
Inspect Shell.

How to set up
=============

Put inspect_shell.py in the directory of the program you want to inspect.

Add
```python
import inspect_shell
```
to the top of that program.

That's it.

How to use
==========

Run your program.  Then run:

    $ python pypandora.py
    
You'll now have an interactive shell to your program.  Anything you do will
affect the program *on the fly.*