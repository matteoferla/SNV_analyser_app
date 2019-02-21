import threading, time


def nothing():
    time.sleep(10)

t=threading.Thread(target=nothing)
t.start()
name=t.name


for i in range(100):
    unfinished_thread_names = [t.name for t in threading.enumerate() if t.name in {name: 'nothing'}.keys()]
    status = [tdescr for tname, tdescr in {name: 'nothing'}.items() if tname in unfinished_thread_names]
    print(threading.enumerate(), unfinished_thread_names,status)
    time.sleep(0.5)
