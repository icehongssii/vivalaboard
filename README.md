# vivalaboard

## 프로젝트 요구 사항

- 회원 CRUD

- 게시판 CRUD

## 프로젝트 로컬에서 시작해보기

DB 실행
```
$ sh up.sh 
```

어플리케이션 실행
```
$ poetry install
$ poetry shell
$ uvicorn app:app --reload
```

게시글 읽어보기

```
$ curl -X 'GET' http://localhost:8000/posts/  -H 'accept: application/json
```

DB 종료 
```
$ sh down.sh
```


## 프로젝트를 하면서 알게 된 점은?

- xxx.icehongssii.xyz (to be continued .. )

## TODO

- CI 파이프라인, tests 폴더 경로 변경/github action 변경

- 게시글 유닛테스트

- 회원 response 타입


## 워크플로우

- 깃허브 프로젝트설정 및 워크플로우 정의

```
#   <타입> 리스트
#   Feat        : 새로운 기능 추가
#   Fix         : 버그 수정
#   Design      : CSS 등 사용자 UI 디자인 변경
#   !BREAKING CHANGE : 커타란 API 변경
#   Style       : 코드 포맷 변경, 세미 콜론 누락 (비즈니스 로직 변경 X)
#   Refactor    : 프로덕션 코드 리팩토링
#   Comment     : 필요한 주석 추가 및 변경
#   Docs        : 문서 수정 (문서 추가, 수정, 삭제, README)
#   Test        : 테스트 추가, 테스트 리팩토링 (비즈니스 로직 변경 X)
#   Chore       : 빌드 태스크 업데이트, 패키지 매니저 설정할 경우 (비즈니스 로직 변경 X)
#   Rename      : 파일 혹은 폴더명을 수정, 옮기는 작업만
#   Remove      : 사용하지 않는 파일 혹은 폴더를 삭제하는 경우
#   Init        : 초기 생성
#


```
- 브랜치 gitflow
	- main
	- develop
	- feature(develop 하위)/상위기능-이슈
- 할일 크게 만들기 (마일스톤단위)
	- 1차 (기본기능)
	- 2차  폴리싱(unittest 및 로깅)
	- 3차 ci/cd 및 배포
- 할일을 작게 쪼개기(이슈단위) 1차 마일스톤 
	- 개발환경
	- 기본회원기능(로그인/회원가입/수정/탈퇴)
	- 기본게시판기능(CRUD/리스팅및소팅)
- 프로젝트 환경설정 중 db 도커파일 만들기

