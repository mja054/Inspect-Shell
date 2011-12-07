#===============================================================================
# Copyright (C) 2011 by Andrew Moffat
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#===============================================================================


import sys
import StringIO
import contextlib
import struct
import traceback
import inspect
import threading
import random
import socket




default_port = 1234




@contextlib.contextmanager
def stdoutIO():
    stdout = StringIO.StringIO()
    old_out = sys.stdout
    sys.stdout = stdout
    yield stdout
    sys.stdout = old_out


class PortInUseException(Exception): pass




def run_shell_server(f_globals, f_locals, port):        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try: sock.bind(("localhost", port))
    except Exception, e:
        if isinstance(e, socket.error) and getattr(e, "errno", False) == 98:
            raise PortInUseException("%d in use" % port)
        else: raise
        
    sock.listen(100)
    #sock.setblocking(0)    
    
    def run_repl(sock):
        while True:
            size = sock.recv(4)
            if not size: return
            size = struct.unpack("i", size)[0]

            code = sock.recv(size)
            if not code: return

            with stdoutIO() as stdout:
                # lets us exec AND eval
                try: exec compile(code, "<dummy>", "single") in f_globals, f_locals
                except: print traceback.format_exc()

            out = stdout.getvalue()
            out = struct.pack("i", len(out)) + out
            sock.send(out)
            
    
    while True:
        new_conn, addr = sock.accept()
        ct = threading.Thread(target=run_repl, args=(new_conn,))
        ct.daemon = True
        ct.start()
        




def open_shell(port):
    sock = socket.socket()
    sock.connect(("localhost", port))
    
    prompt = "is:%d> " % port

    while True:
        line = raw_input(prompt)
        data = struct.pack("i", len(line)) + line
        sock.send(data)

        size = sock.recv(4)
        if not size: return
        size = struct.unpack("i", size)[0]

        if size:
            reply = sock.recv(size)
            print reply
            
            



# running from commandline, open a shell
if __name__ == "__main__":
    try: port = int(sys.argv[1])
    except: port = default_port
    open_shell(port)
    
# it's being imported, run the shell server
else:
    caller = inspect.stack()[1][0]
    f_globals = caller.f_globals
    port = f_globals.get("inspect_shell_port", default_port)
    
    st = threading.Thread(target=run_shell_server, args=(f_globals, caller.f_locals, port))
    st.daemon = True
    st.start()
    