import pickle

f = open('somedata', 'wb')


class A():
    class B():
        y = 2

    b = B()
    x = 1


a = pickle.dump(A(), f)

f = open('somedata', 'rb')
a_ = pickle.load(f)
print(a_.x)
print(a_.B.y)
print(a_.b.y)
