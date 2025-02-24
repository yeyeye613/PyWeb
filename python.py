import json
"""
json.dump(obj, file)：将Python对象序列化为JSON格式并写入文件。
json.dumps(obj)：将Python对象序列化为JSON格式的字符串。
json.load(file)：从文件中读取JSON数据并转换为Python对象。
json.loads(json_string)：从JSON格式的字符串中读取数据并转换为Python对象。
"""
dict_obj = {"name": "John", "age": 30, "city": "New York"}
data = dict_obj
# 打开文件以写入
"""

"""
with open('data.json', 'w') as file:
    # 使用json.dump()将数据写入文件
    json.dump(data, file)

# dumps()方法将数据转换为JSON格式的字符串
json_string = json.dumps(data)
print(json_string)

"""
python语法解析
"""
# print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
print("helloworld")

