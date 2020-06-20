# This program generate pure number dictionary for brute-force attack wifi password

import sys


# This program generate pure number dictionary for brute-force attack wifi password
# recommend : https://github.com/search?q=wifi+dictionary
def main():
    print("WARNING : file will create in the current directory.\n")
    num_digit = input("num digit:(default:8)")
    if not num_digit:
        num_digit = 8
    start = input("start num:(default:00000000)")
    if not start:
        start = 0
    end = input("end num:(default:100000000)(not include)")
    print()
    if not end:
        end = 100000000
    try:
        num_digit = int(num_digit)
        start = int(start)
        start_ = start
        end = int(end)
    except:
        print("start and end should be number")
        sys.exit(1)
    if start >= end:
        print("start should be smaller than end")
        sys.exit(2)
    if len(str(end - 1)) > num_digit:
        print("if end bigger than 1e{}(num_digit) , some number will miss".format(num_digit))
        sys.exit(3)

    data_size = 1
    if end - start >= 100:
        data_size = 100  # 1e2
    elif end - start >= 10000:
        data_size = 10000  # 1e4
    elif end - start >= 1000000:
        data_size = 1000000  # 1e6
    elif end - start >= 10000000:
        data_size = 1000000  # 1e7

    with open("pure_digits.txt", 'w+') as f:
        exit_flag = False
        while True:
            data = []
            one_loop_end = start + data_size
            if one_loop_end > end:
                one_loop_end = end
                exit_flag = True
            for i in range(start, one_loop_end):
                data.append(str(i).zfill(num_digit) + "\n")
            f.writelines(data)
            start = one_loop_end
            if exit_flag:
                break
            print("{}%".format(int((one_loop_end - start_) / (end - start_) * 100)), end="\r")


if __name__ == '__main__':
    main()
