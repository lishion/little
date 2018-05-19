import os
from time import sleep
from mini_cache import mini_cache
class manager(object):
    def __init__(self,filename,block_size):
        self._filename = filename
        self._block_size = block_size
        self._block_dir = "." + self._filename
        self.__split_delimiter = "-@@-"
        self._current_blockindex = 0
        self._max_blockindex = 0
        self._cache = mini_cache.mini_cache("."+self._filename+"_cache")

    #清除文件夹及其文件
    def clear_blocks(self):
        if self.__dir_exist():
            blocks = os.listdir(self._block_dir)
            try:
                for index, in enumerate(blocks):
                    os.remove(self.__block_name(index))
            except:
                pass
            os.rmdir(self._block_dir)
        self._cache.clear()

    def __dir_exist(self):
        return os.path.exists(self._block_dir)

    def __block_name(self, block_index):
        return self._block_dir + os.sep + self._filename + self.__split_delimiter + str(block_index)

    def __split(self):
        assert not self.__dir_exist()
        assert os.path.exists(self._filename)
        os.mkdir(self._block_dir)
        with open(self._filename,'r') as main_file:
            block = open(self.__block_name(0),'w')
            block_index = 0
            for index,line in enumerate(main_file):
                block.writelines(line)
                start_new_block = index % self._block_size == self._block_size - 1
                if start_new_block:
                    block.flush()
                    block.close()
                    block_index = index // self._block_size + 1
                    block = open(self.__block_name(block_index) ,'w')
            self._cache.cache("max_block_index",block_index)

    def split_if_not_exist(self):
        if not self.__dir_exist():
            if not os.path.exists(self._filename):
                raise Exception(f"no file named {self._filename}")
            self.__split()

    # 获取正在处理的文件名
    def current_blockname(self):
        return self.__block_name(self._current_blockindex)
    
    #获取所有文件的迭代器
    def blocks(self):
        while self._current_blockindex <= self._max_blockindex:
            try:
                self._cache.cache("current_blockindex",self._current_blockindex)
                yield open(self.current_blockname(),'r')
            except Exception as e:
                print(f" error:{e.args[1]}, skip file {self.current_blockname()}")
            finally:
                self._current_blockindex += 1
                
    # 从缓存中恢复正在处理的文件        
    def recover_from_cache(self):
        data = self._cache.uncache()
        self._current_blockindex = int(data.get("current_blockindex",0))
        self._max_blockindex = int(data.get("max_block_index",0))
   


        

  
   
          


    