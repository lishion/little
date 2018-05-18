import json
import os
 
cache_file_name = ".mini.cache"

def is_cache_exist():
    return os.path.exists(cache_file_name)

def cache(key,value):
    if not is_cache_exist():
        with open(cache_file_name,"w") as f:
            json.dump({key:value},f)
    else:
        with open(cache_file_name,'r') as f:
            data = json.load(f)
        data[key] = value
        with open(cache_file_name,'w') as f:
            json.dump(data,f)
    
def uncache():
    if not is_cache_exist():
        raise Exception('no cache file find! ensure you have cached some something!')
    with open(cache_file_name,'r') as f:
        return  json.load(f)

def clear():
    if is_cache_exist():
        os.remove(cache_file_name)

def get(key):
    return uncache()[key]

if __name__ == "__main__":
    clear()
    cache("num",23423)
    cache("aaa",123)
    print(get("num"),get("aaa"))