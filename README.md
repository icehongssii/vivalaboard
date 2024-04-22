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