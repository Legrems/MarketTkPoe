import re
import sys
import ctypes

c_ptrace = ctypes.CDLL("libc.so.6").ptrace
c_pid_t = ctypes.c_int32
# This assumes pid_t is int32_t
c_ptrace.argtypes = [ctypes.c_int, c_pid_t, ctypes.c_void_p, ctypes.c_void_p]
PTRACE_ATTACH = 16
PTRACE_DETACH = 17


def ptrace(attach, pid):
    op = ctypes.c_int(PTRACE_ATTACH if attach else PTRACE_DETACH)
    c_pid = c_pid_t(pid)
    null = ctypes.c_void_p()
    err = c_ptrace(op, c_pid, null, null)
    if err != 0: raise RuntimeError('ptrace', err)

if (len(sys.argv) < 2):
    print(("Usage %s <pid>" % sys.argv[0]), file=sys.stderr)
else:
    pid = int(sys.argv[1])
    ptrace(True, pid)
    mappath = "/proc/%s/maps" % (pid)
    mempath = "/proc/%s/mem"  % (pid)
    outpath = "/tmp/dump.dat"
    with open(mappath, 'r') as maps_file:
        memmap = maps_file.readlines()
    mem_file  = open(mempath, 'rb', 0)
    out_file  = open(outpath,  'wb')
    i = 0
    for line in memmap:
        m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r])', line)
        if m.group(3) == 'r':
            start   = int(m.group(1), 16)
            end     = int(m.group(2), 16)
            try:
                pos     = mem_file.seek(start)
                chunk   = mem_file.read(end - start)
                print(("Read Line: %s" % (line)), file=sys.stderr)
            except:
                print(("Could not read: %016x" % (pos)), file=sys.stderr)
                print(("Line: %s" % (line)), file=sys.stderr)
                pass
            result = out_file.write(chunk)
    print(("Wrote file: %s" % (outpath)), file=sys.stderr)
    out_file.close()
    mem_file.close()
    ptrace(False, pid)