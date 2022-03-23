## 로컬 실행 방법
#### 프로젝트 폴더 내 가상환경 설치 및 실행
* pip install virtualenv
* virtualenv venv
* source venv/bin/activate
#### 의존성 라이브러리 설치 후 migrate 수행
* pip install -r requirement.txt
* python manage.py migrate
#### 서버 실행
* python manage.py runserver


## 사용기술
* Python : 3.8.8
* Django : 4.0.3
* djangorestframework : 3.13.1
* sqlite3


## API Document
* Link: https://documenter.getpostman.com/view/19243168/UVsQu5BM


## 기능 요구사항 구현 범위
### 전화번호 인증
- 전화 번호를 입력하면 6자리 숫자의 인증번호를 발급
- 인증번호는 만료 시간이 발급 후 5분으로 설정되고, 5분 내에 재발급은 불가능하도록 구현

### 회원가입
* 이메일, 비밀번호, 닉네임, 이름, 전화번호, 인증 번호를 입력하여 회원가입 진행

* 기본 제약사항
    - 발급받은 인증번호와 입력한 인증번호가 일치하지 않으면 회원가입이 불가능
    - 인증번호가 만료되면 회원가입 진행이 불가능하며 인증번호 재발급 후 회원가입을 해야 함
    - 입력한 비밀번호와 재확인용으로 입력한 비밀번호가 일치하지 않으면 회원가입이 불가능
    - 입력한 이메일, 닉네임, 전화번호가 이미 가입된 회원 정보와 동일하면 회원가입 불가능

* 비밀번호 제약사항
    - 8자 이상 12자 이하로 길이가 제한됨
    - 영문 + 숫자 조합으로 만들어야 함
    - 이메일 앞자리 혹은 닉네임과 동일하게 설정이 불가능

### 로그인
* 세션/쿠키 방식으로 로그인이 처리됨
* 식별가능한 정보 중 이메일과 비밀번호를 입력받음
* 이메일 혹은 비밀번호가 올바르지 않으면 로그인이 불가능

### 내 정보 보기 
* 로그인된 회원 본인의 이메일, 닉네임, 이름, 전화번호 정보 조회가 가능(비밀번호 제외)

### 비밀번호 재설정 기능
* 회원가입 시와 동일한 전화번호 인증 API를 통해 전화번호 입력 후 인증번호 발급
* 로그인된 상태에서는 접근이 불가능
* 인증번호와 이메일 주소, 새 비밀번호를 입력하면 비밀번호 재설정 가능
* 인증번호가 만료되면 인증번호 재발급이 필요
* 인증번호가 올바르지 않으면 비밀번호 재설정이 불가능
* 입력한 이메일 주소가 올바르지 않으면 비밀번호 재설정이 불가능

