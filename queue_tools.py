import queue
from concurrent.futures import ThreadPoolExecutor
import time
# 利用queu并发执行
# 构造函数:
#     method:需要并发执行的方法
#     thread_num:线程数，默认10
# methon第一个参数会被传入队列剩余的元素， 剩下多个参数，请使用数组或字典的方式将数据写入队列，参看Demo

class resolver(object):

    def __init__(self,method,has_return=True,thread_num=10):
        self.executors = ThreadPoolExecutor(thread_num)
        self.thread_num = thread_num
        self.method = method
        self.rq = queue.Queue()
        self.wq = queue.Queue()
        self.has_return = has_return
        self.has_done = 0
 
    # 执行线程
    # 调用该方法前必须调用fetch_data获取数据!!!!
    def do(self):
  
        for i in range(0,self.thread_num):
            self.executors.submit(self.__method_warper)
        self.rq.join()
        self.executors.shutdown()
        return self

    # 读取数据到队列中，data可以是一个迭代器或则数组
    # processer: 放入前对data进行处理的函数，确保不会抛出异常!!
    def fetch_data(self,data,processer=None):
        
        for item in data:
            if processer:
                self.rq.put(processer(item))
            else:
                self.rq.put(item)
        
    # 以queue的方式返回执行结果
    def results_queue(self):
        return self.wq

    # 以队列的方式返回执行结果
    def results_list(self):
        return self.__queue_to_list(self.wq)
    
    def __method_warper(self):
        while True:
            if self.rq.empty():
                return
            try:
                args = self.rq.get()
                surplus_num = self.has_done
                if type(args) == list:
                    o = self.method(surplus_num,*args)
                elif type(args) == dict:
                    o = self.method(surplus_num,**args)
                else:
                    o = self.method(surplus_num,args)
                if self.has_return:
                    self.wq.put(o)
            except BaseException as e:
                print(e)
            finally:
                self.has_done += 1
                self.rq.task_done()

    def __queue_to_list(self,q):
        data = []
        while not q.empty():
            data.append(q.get())
        return data

if __name__=="__main__":
    def test(num,param1,param2):
        return param1 + param2
        
    x = [{"param1":x,"param2":x+1} for x in range(1,1600)]
    r = resolver(test) 
    r.fetch_data(x)
    r.do()
 
     


    
