# from multiprocessing import Pool
# 
# def f(x):
#     return x*x
# 
# if __name__ == '__main__':
#     p = Pool(1)
#     print(p.map(f, [1, 2, 3]))


# from multiprocessing import Process
# import os
# 
# def info(title):
#     print title
#     print 'module name:', __name__
#     if hasattr(os, 'getppid'):  # only available on Unix
#         print 'parent process:', os.getppid()
#     print 'process id:', os.getpid()
# 
# def f(name):
#     info('function f')
#     print 'hello', name
# 
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()


from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print parent_conn.recv()   # prints "[42, None, 'hello']"
    p.join()