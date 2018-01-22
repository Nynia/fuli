results = [{'url': 'http://www.baidu.com', 'path': ''}, {'url': 'http://www.163.com', 'path': '/opt2'}]

file_paths = [x['path'] for ok, x in results if ok]
print file_paths
