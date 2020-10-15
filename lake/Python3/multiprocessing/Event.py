#  multiprocessing Event usage

#  https://docs.python.org/3.7/library/multiprocessing.html#multiprocessing.Event

#  use event dont will block process like time.sleep()

import time
import multiprocessing as mp

def wait_for_event(e):
    event_is_set = e.wait()
    print("function wait_for_event finish")
    print(e.is_set())
    # set e as false
    e.clear()

# init
e = mp.Event()

# create process
p = mp.Process(target=wait_for_event,args=(e,))

# start
p.start()

# set e as true
e.set()

time.sleep(1)

# check e status
print(e.is_set())







Event Objects¶
This is one of the simplest mechanisms for communication between threads: one thread signals an event and other threads wait for it.

An event object manages an internal flag that can be set to true with the set() method and reset to false with the clear() method. The wait() method blocks until the flag is true.

class threading.Event
Class implementing event objects. An event manages a flag that can be set to true with the set() method and reset to false with the clear() method. The wait() method blocks until the flag is true. The flag is initially false.

Changed in version 3.3: changed from a factory function to a class.

is_set()
Return true if and only if the internal flag is true.

set()
Set the internal flag to true. All threads waiting for it to become true are awakened. Threads that call wait() once the flag is true will not block at all.

clear()
Reset the internal flag to false. Subsequently, threads calling wait() will block until set() is called to set the internal flag to true again.

wait(timeout=None)
Block until the internal flag is true. If the internal flag is true on entry, return immediately. Otherwise, block until another thread calls set() to set the flag to true, or until the optional timeout occurs.

When the timeout argument is present and not None, it should be a floating point number specifying a timeout for the operation in seconds (or fractions thereof).

This method returns true if and only if the internal flag has been set to true, either before the wait call or after the wait starts, so it will always return True except if a timeout is given and the operation times out.

Changed in version 3.1: Previously, the method always returned None