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

def search_keyword(lines, kw_include, kw_exclude = [],\
             include_only_need_one = False, include_idx = False):

    count = 0
    found_lines = []

    if type(kw_include) is str: kw_include = [kw_include]
    if type(kw_exclude) is str: kw_exclude = [kw_exclude]   
        
    for idx, line in enumerate(lines):
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
        if not include_idx:
            found_lines.append(line)
        else:
            found_lines.append((line, idx))

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

def output_a(lines):
    line_num = 1

    stat_pid = -1
    stat_line_num = -1
    stat_line = ''
    
    for line in lines:
        if 'stat(' in line:
            
            stat_line_num = line_num
            stat_pid = line.split()[0]
            stat_line = line

        elif 'clone(' in line:
            clone_line_num = line_num
            clone_pid = line.split()[0]
            clone_line = line

            if clone_pid == stat_pid:
                print(str(stat_line_num) + '\t' + stat_line)
                print(str(clone_line_num) + '\t' + clone_line)
                
                stat_pid = -1
                stat_line_num = -1
                stat_line = ''

        line_num += 1

def output_c(lines):
    pass

def main():
    log_a_name = 'Log-A.strace'
    lines_a = read_file(log_a_name)

    log_b_name = 'Log-B.strace' 
    lines_b = read_file(log_b_name)

    print('output a')
    output_a(lines_a)

    print('output b')
    output_a(lines_b)

    print('output c')
    output_c(lines_a)
    output_c(lines_b)


if __name__ == '__main__':
    main()