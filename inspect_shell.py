import sys
import StringIO
import contextlib
import eventlet
import struct
import traceback
import inspect
import threading
import random
import socket



@contextlib.contextmanager
def stdoutIO():
    stdout = StringIO.StringIO()
    old_out = sys.stdout
    sys.stdout = stdout
    yield stdout
    sys.stdout = old_out


class PortInUseException(Exception): pass


def run_shell_server(port=1234):
    caller = inspect.stack()[1][0]
    try: server = eventlet.listen(("localhost", port))
    except Exception, e:
        if isinstance(e, socket.error) and getattr(e, "errno", False) == 98:
            raise PortInUseException("%d in use" % port)
        else:r raise

    def run_repl(sock):
        while True:
            size = sock.recv(4)
            if not size: return
            size = struct.unpack("i", size)[0]

            code = sock.recv(size)
            if not code: return

            with stdoutIO() as stdout:
                # lets us exec AND eval
                try: exec compile(code, "<dummy>", "single") in caller.f_globals, caller.f_locals
                except: print traceback.format_exc()

            out = stdout.getvalue()
            out = struct.pack("i", len(out)) + out
            sock.send(out)


    pool = eventlet.GreenPool()
    while True:
        sock, addr = server.accept()
        pool.spawn_n(run_repl, sock)



def open_shell(port=1234):
    sock = socket.socket()
    sock.connect(("", port))

    while True:
        line = raw_input("rs> ")
        data = struct.pack("i", len(line)) + line
        sock.send(data)

        
        size = sock.recv(4)
        if not size: return
        size = struct.unpack("i", size)[0]

        if size:
            reply = sock.recv(size)
            print reply



if __name__ == "__main__":
    open_shell()
    
else:
    while True:
        port = random.randint(1024, 64000)
        try:
            run_shell_server()
            break
        except PortInUseException: continue