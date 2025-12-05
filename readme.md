동국대학교 공개SW프로젝트 2분반 7조의 Github입니다.
## 영화 데이터 불러오기

영화 정보 CSV 데이터 불러오는 명령어:

```bash
# Django 쉘 실행
python manage.py shell

# load_csv 모듈에서 run 함수 실행
from movies.load_csv import run
run()
