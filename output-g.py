f = open('Log-A.strace')
lines = f.readlines()

term = ' read('
term2 = 'pipe'
term3 = 'tty'

def extract_name(line, start_delimiter, end_delimiter):

    name_start = line.find(start_delimiter)
    name_end = line.find(end_delimiter, name_start + 1)
    name = line[name_start + 1 : name_end]
    return name

names = []
counts = []

for line in lines:
    if 'read(' in line and 'pipe' not in line and 'tty' not in line:
        name = extract_name(line, '<', '>')

        if name not in names:
            names.append(name)
            counts.append(1)
        
        else:
            idx = names.index(name)
            counts[idx] += 1

for i in range(len(names)):
    name = names[i]
    count = counts[i]
    #print(name, count)
    print(name + '\t' + str(count))


# example output

# ('/lib/x86_64-linux-gnu/libc-2.23.so', 4)
# ('/etc/nsswitch.conf', 4)
# ('/lib/x86_64-linux-gnu/libnss_compat-2.23.so', 2)
# ('/lib/x86_64-linux-gnu/libnsl-2.23.so', 2)
# ('/lib/x86_64-linux-gnu/libnss_nis-2.23.so', 2)
# ('/lib/x86_64-linux-gnu/libnss_files-2.23.so', 2)
# ('/lib/x86_64-linux-gnu/libselinux.so.1', 1)
# ('/lib/x86_64-linux-gnu/libpcre.so.3.13.2', 1)
# ('/lib/x86_64-linux-gnu/libdl-2.23.so', 1)
# ('/lib/x86_64-linux-gnu/libpthread-2.23.so', 1)
# ('/proc/filesystems', 2)
# ('/etc/locale.alias', 2)
# ('/proc/sys/kernel/ngroups_max', 2)