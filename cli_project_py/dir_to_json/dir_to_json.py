from pathlib import Path
from datetime import datetime
import json


# 프로그램 실행 위치에서 디렉토리 정보를 json 파일로 변환해 저장하기
# referrence 
# python 3.7 standard library 
# https://docs.python.org/3.7/library/
## open(): built-in function
## pathlib:Object-oriented filesystem paths module 
## datetime: Basic date and time types
## json: Internet Data Handling module
## dict: built-in sequence type
## list: built-in mapping type


    
# 디렉토리 정보를 저장할 리스트
dirData = []
# 프로그램이 실행된 현재 위치로 path 객체 생성
p = Path()

# 디렉토리 정보를 dirData에 저장
if p.is_dir():
    for x in p.iterdir():
        name = x.name 
        dt = datetime.fromtimestamp(x.stat().st_mtime)
        changed = dt.strftime('%Y-%m-%d %I:%M%p')
        size = str(x.stat().st_size) + ' byte'
        if x.is_file(): 
            filetype = '<FILE>'
        else:
            filetype = '<DIR>'

        row = {'name': name, 'changed': changed, 'size': size, 'type': filetype}
        dirData.append(row) 



today = datetime.today().strftime('%Y%m%d%I%M%S')

# 쓰기 A. file object를 반환하는 open() 내장함수 이용 
filename = 'dir_info_A_'+today+'.json'
where = Path(p / filename)

f = open(where,'w')
json.dump(dirData, f, indent=4)

# 쓰기 B. pathlib의 write_text() 함수 이용
filename = 'dir_info_B_'+today+'.json'
where = Path(p / filename)

js = json.dumps(dirData, indent=4)
where.write_text(js)

print('현재 위치에 파일이 저장되었습니다.')







## 부록: 하위 디렉토리까지 모두 탐색해서 출력
def findSubDirectory(path):
    if path.is_dir():
        for x in path.iterdir():
            print(x)
            sub = Path(x)
            findSubDirectory(sub)

