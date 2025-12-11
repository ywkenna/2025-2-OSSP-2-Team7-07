동국대학교 공개SW프로젝트 2분반 7조의 Github입니다.

# 다양한 언어적 특성을 기반으로 한 영화 속 영어 난이도 평가 서비스


## 프로젝트 소개
최근 영어 회화 학습은 다양한 온라인 영상 콘텐츠를 활용하는 형태로 확산되고 있지만, 영화 속 영어의 난이도를 평가하는 방법에 대한 정답은 현재 존재하지 않는다.
본 프로젝트에서는 영화의 난이도를 분석하고, 이 난이도를 기반으로 사용자가 자신에게 맞는 영화를 선택할 수 있도록 도움을 주는 사이트를 제공한다.

## 영어 영화 난이도 분석 모델
본 조는 영어 영화 난이도를 분석하는 모델을 만들기 위하여 단어의 난이도, 중첩 발화 비율, 과거분사 비율, 발음 명료성 등 총 13개의 지표를 분석하였으며, 주요 지표 6종을 사용하여 최종 모델을 설계하였다.<br>
<br><p align="center">
  <img src="https://github.com/user-attachments/assets/90b52b1a-ad18-4823-a86a-b5785a379386"
       width="450">
</p><br>
<br>LogitBoost 모델을 사용하였으며, 설계된 모델은 76%의 정확도를 가지고 있다.





## 기능
### 1. 영화 기본 정보
<img src="https://github.com/user-attachments/assets/a9712989-ce23-4448-95e1-c92ce299d06f" width="600">
<br><br>
본 조에서 분석한 50종의 영화에 대한 리스트 및 기본 정보를 홈화면에서 확인할 수 있다. 기본 정보는 영화 포스터, 제목, 런타임, 장르 및 본 조가 직접 도출한 난이도(LogitBoost 사용)를 포함한다. 

### 2. 영화 필터링 및 검색
<img src="https://github.com/user-attachments/assets/04fec936-ef1a-49e4-8dcb-351450313788" width="200">
<br><br>
사용자는 원하는 영화를 검색할 수 있으며, 장르, 난이도, 개봉년도 별로 필터링 할 수 있다. 

### 3. 영화 상세페이지

<img src="https://github.com/user-attachments/assets/ba6b8674-62ca-43a9-b58e-9f23e6692e18" width="800">
<img src="https://github.com/user-attachments/assets/562f3ed7-920a-4802-bfb4-719d7f0869f4" width="600">
<br><br>
선택한 영화에 대하여 줄거리와 OTT 링크를 포함한 상세 정보를 확인할 수 있으며, 본 조가 분석한 해당 영화의 지표별 수치를 그래표 형태로 제공받을 수 있다. 

### 4. 사용자 영어 성적 입력
<img src="https://github.com/user-attachments/assets/bbd7cbea-2ecb-4bfc-88fe-b08236c0c055" width="700">
<br><br>
사용자는 본인의 공인 영어 성적을 입력하여 본 사이트에서 사용하고 있는 기준으로 변환된 자신의 레벨을 확인할 수 있다. 위에서 기술한 필터링 기능을 통해 자신의 레벨에 해당하는 영화를 추천받을 수 있다.  

### 5. 영화 리뷰 및 찜 기능
<img src="https://github.com/user-attachments/assets/8b09e413-c88f-4b2c-ae2e-4cb087d0d204" width="500">
<img src="https://github.com/user-attachments/assets/8dc59a25-bf6f-4836-86bd-10f80cbebe0d" width="500">

<br><br>
사용자는 영화에 대한 리뷰를 통해 자신이 해당 영화에 대하여 느낀 난이도 등을 다른 사람과 공유할 수 있으며, 찜 기능을 통해 원하는 영화를 마이페이지에 저장할 수 있다.

## 기술 스택
### **Frontend**
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

### **Backend**
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20API-005571?logo=fastapi&logoColor=white)

### **Database**
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

### **ML**
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?logo=spacy&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154D71?logo=python&logoColor=white)

## 팀원 소개
|이름        |학과        |역할        |
|-----------|-------------|------------|
|김예원|컴퓨터공학전공|팀장|
|박지현|컴퓨터AI학부|팀원|
|박채훈|컴퓨터공학전공|팀원|
|박혜란|멀티미디어소프트웨어공학|팀원|
|이경민|컴퓨터AI학부|팀원|

