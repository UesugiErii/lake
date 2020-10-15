# This program generate letter and birthday combination dictionary for brute-force attack wifi password
import string

start_year = 1950
stop_year = 2020
birthday = []
for y in range(start_year, stop_year):
    for m in range(1, 13):
        for d in range(1, 32):
            s1 = str(y)
            s2 = str(m)
            s3 = str(d)
            if len(s2) < 2:
                s2 = "0" + s2
            if len(s3) < 2:
                s3 = "0" + s3
            birthday.append(s1 + s2 + s3)

first_row = "qwertyuiop"
second_row = "asdfghjkl"
third_row = "zxcvbnm"
common_arrangement = []
for l in range(4, 8):
    for s in [first_row, second_row, third_row]:
        for i in range(0, len(s) - l + 1):
            common_arrangement.append(s[i:i + l])


def f0(f):
    for i in common_arrangement:
        temp = []
        for j in birthday:
            temp.append(i + j + "\n")
            temp.append(j + i + "\n")
        f.writelines(temp)


def f1(f):
    for i in string.ascii_letters:
        temp = []
        for j in birthday:
            temp.append(i + j + "\n")
            temp.append(j + i + "\n")
        f.writelines(temp)


def f2(f):
    for i in string.ascii_letters:
        for k in string.ascii_letters:
            temp = []
            t = i + k
            for j in birthday:
                temp.append(t + j + "\n")
                temp.append(j + t + "\n")
            f.writelines(temp)


def f3(f):
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            for k in string.ascii_lowercase:
                temp = []
                t = i + j + k
                for b in birthday:
                    temp.append(t + b + "\n")
                f.writelines(temp)


def f4(f):
    for i in string.ascii_uppercase:
        for j in string.ascii_uppercase:
            for k in string.ascii_uppercase:
                temp = []
                t = i + j + k
                for b in birthday:
                    temp.append(t + b + "\n")
                f.writelines(temp)


def f5(f):
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            for k in string.ascii_lowercase:
                temp = []
                t = i + j + k
                for b in birthday:
                    temp.append(b + t + "\n")
                f.writelines(temp)


def f6(f):
    for i in string.ascii_uppercase:
        for j in string.ascii_uppercase:
            for k in string.ascii_uppercase:
                temp = []
                t = i + j + k
                for b in birthday:
                    temp.append(b + t + "\n")
                f.writelines(temp)


def main():
    choice = input("""0. common arrangement + birthday and birthday + common arrangement
1. one letter + birthday and birthday + one letter (10 years 3.7MB)
2. two letters + birthday and birthday + two letters  (10 years  214.2MB) 
3. three lowercase letters + birthday  (10 years  759.3MB) 
4. three capital letters + birthday
5. birthday + three lowercase letters
6. birthday + three capital letters
"""
                   )
    choice = int(choice)

    f = open("dict.txt", 'w+')
    try:
        if choice == 0:
            f0(f)
        elif choice == 1:
            f1(f)
        elif choice == 2:
            f2(f)
        elif choice == 3:
            f3(f)
        elif choice == 4:
            f4(f)
        elif choice == 5:
            f5(f)
        elif choice == 6:
            f6(f)
    finally:
        f.close()


if __name__ == '__main__':
    main()
