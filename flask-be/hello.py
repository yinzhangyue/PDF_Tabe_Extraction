# print('hello world')
import json
if __name__ == '__main__':
    with open('./upload/Financial.json') as f:
        data = json.load(f)
    print(str(data))