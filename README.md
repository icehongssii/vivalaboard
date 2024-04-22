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


## TODO
- 