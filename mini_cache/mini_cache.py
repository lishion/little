import json
import os
 
class mini_cache(object):
     
    def __init__(self,filename):
        self._cache_filename = filename

    def __is_cache_exist(self):
        return os.path.exists(self._cache_filename)

    def cache(self,key,value):
        try:
            if not self.__is_cache_exist():
                with open(self._cache_filename,"w") as f:
                    cache_data = json.dumps({key:value})
                    f.writelines(cache_data)
            else:
                with open(self._cache_filename,'r') as f:
                    data = json.load(f) or {}
                data[key] = value
                with open(self._cache_filename,'w') as f:
                    cache_data = json.dumps(data)
                    f.writelines(cache_data)
        except Exception:
            raise Exception(f"cache failed")
        
    def uncache(self):
        if not self.__is_cache_exist():
            raise Exception('no cache file find! ensure you have cached some something')
        try:
            with open(self._cache_filename,'r') as f:
                return  json.load(f)
        except Exception:
            raise Exception('parse cache file failed')

    def clear(self):
        if self.__is_cache_exist():
            os.remove(self._cache_filename)

    def get(self,key):
        return self.uncache()[key]

    