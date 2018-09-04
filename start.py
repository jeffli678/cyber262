#encoding: utf-8
import sys

def read_file(file_name):

    lines = None
    try:
        with open(file_name) as f:
            lines = f.read().splitlines()
    except:
        print('file "%s" does not exitst, please check...' % file_name)
        sys.exit(0)
    
    return lines

def search_keyword(lines, kw_include, kw_exclude = [], include_only_need_one = False):

    count = 0
    found_lines = []

    if type(kw_include) is str: kw_include = [kw_include]
    if type(kw_exclude) is str: kw_exclude = [kw_exclude]
        
    for line in lines:
        try:
            include_found = False
            for kw in kw_include:
                if not kw in line:
                    if not include_only_need_one:
                        raise StopIteration
                else:
                    include_found = True
            if include_only_need_one and not include_found:
                raise StopIteration
            
            for kw in kw_exclude:
                if kw in line:
                    raise StopIteration

        except StopIteration:
            continue

        count += 1
        found_lines.append(line)

    return (count, found_lines)

def print_lines(lines):
    for line in lines:
        print(line)

def search_both_log(lines_a, lines_b, kw_include, kw_exclude = [], \
                    include_only_need_one = False):

    count_a, _ = search_keyword(lines_a, kw_include, kw_exclude, include_only_need_one)
    count_b, _ = search_keyword(lines_b, kw_include, kw_exclude, include_only_need_one)
    return (count_a, count_b)

def extract_program_name(line, start_delimiter, end_delimiter):

    name_start = line.find(start_delimiter)
    name_end = line.find(end_delimiter, name_start + 1)
    name = line[name_start + 1 : name_end]
    return name

def output_a(lines_a, lines_b):

    a, b = search_both_log(lines_a, lines_b, ' read(', ['tty', 'pipe'])
    print(a, b)

    a, b = search_both_log(lines_a, lines_b, [' read(', 'tty'])
    print(a, b)

    a, b = search_both_log(lines_a, lines_b, [' read(', 'pipe'])
    print(a, b)

    print('\n')

def output_b(lines_a, lines_b):

    a, b = search_both_log(lines_a, lines_b, ' execve(')
    print(a, b)

    a, b = search_both_log(lines_a, lines_b, ' write(')
    print(a, b)

    # treat stat as the same as fstat
    a, b = search_both_log(lines_a, lines_b, [' access(', 'stat('], \
                            include_only_need_one = True)
    print(a, b)

    a, b = search_both_log(lines_a, lines_b, ' unlinkat(')
    print(a, b)

    a, b = search_both_log(lines_a, lines_b, ' exit_group(')
    print(a, b)\

    print('\n')

def output_c(lines_a, lines_b):
    a, ret_a = search_keyword(lines_a, ' execve(')
    print_lines(ret_a)
    for line in ret_a:
        name = extract_program_name(line, '"', '"')
        print(name)
    
    print('\n')
    
    b, ret_b = search_keyword(lines_b, ' execve(')
    print_lines(ret_b)


def main():
    log_a_name = 'Log-A.strace'
    lines_a = read_file(log_a_name)

    log_b_name = 'Log-B.strace' 
    lines_b = read_file(log_b_name)

    output_a(lines_a, lines_b)
    output_b(lines_a, lines_b)
    output_c(lines_a, lines_b)


if __name__ == '__main__':
    main()