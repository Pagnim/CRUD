## [위코드 x 원티드] 백엔드 프리온보딩 선발 과제
>### 글 작성, 글 확인, 글 목록 확인, 글 수정, 글 삭제 기능
- #### ♢SECRET_KEY와 ALGORITHM은 깃 허브에 업로드 하기 위해 .gitignore파일에 따로 저장해두었습니다.

>- #### 회원가입
    - method : **Post**
    - http://127.0.0.1:8000/users/signup
    -   ```
        body : {
                "name":"name",
                "password":"password"
        }
        ```
    - success response : {"message": "CREATED!"}
    - 프론트가 body 값에 name과 password를 보내주면 User테이블에 데이터를 생성합니다.
    - password는 bcrypt와 salt를 이용해 좀 더 복잡하게 암호와하여 데이터 베이스에 저장하였습니다.
    - 데이터베이스에 string형태로 저장하기위해 인코딩한 후 다시 디코딩하여 넣어주었습니다.
    - 같은 이름으로 가입하는 것을 막기 위해 name에 uniqe=True를 주었습니다.
    - 같은 이름으로 가입하면 401에러를 반환하였습니다.

>- #### 로그인
    - method : **post**
    - http://127.0.0.1:8000/users/signin
    -   ```
        body : {
                "name" : "가입된 name",
                "password":"가입된 password"
        }
        ```
    - success response : {"access_token" : access_token}
    - 프론트가 body 값에 name과 password를 보내주면
    - name은 데이터베이스에 있는 값과 일치하면 다음 코드로 없으면 "message" : "DO NOT EXIST!"과 함께 401에러를 출력하였습니다.
    - 만약 데이터베이스에 있으면 그 name과 일치하는 password를 bcrypt로 인코딩하고 body에서 들어온 password의 인코딩 값이 같은지 확인하였습니다.
    - 값이 일치하면 jwt를 이용해 유저의 id값 시크릿키 알고리즘을 인코딩하여 access_token을 생성하였습니다.
    - 프론트가 나중에 토큰값을 사용할 수 있게 토큰 값을 보내주었습니다.


>- #### 글 작성
    - method : **post**
    - http://127.0.0.1:8000/posts/post
    -   ```
        body : {
                "title" : "제목",
                "content" : "내용"
        }
        ```
    - success response : {"message":"CREATED!"}
    - 프론트가 body 값에 title과 content를 보내주면 Post테이블에 title, content를 생성합니다.
    - 또한 login_decorator를 통해 해당 유저의 id와 이름을 가져와서 같이 테이블에 넣어 무슨 유저가 쓴 글인지 알수있게 하였습니다.

>- #### 글 목록 보기
    - method : **get**
    - http://127.0.0.1:8000/posts/read/0?page=1 (전체 글 보기)
     success response : ```
                {
                "data": {
                    "count": 13,
                    "posts": [
                        {
                            "user": "pang",
                            "title": "수정제목",
                            "user_id": 1
                        },
                        {
                            "user": "pang",
                            "title": "제목2",
                            "user_id": 1
                        }
                       }
                      ]
                }
                ```
    - http://127.0.0.1:8000/posts/read/<int:posts_id>
     success response : ```
                {
                "data": {
                    "post_id": 1,
                    "user": "pang",
                    "title  ": "수정제목",
                    "content": "수정 내용"
                }
            }
            ```
    - 프론트가 get요청을 보내 총 게시글, 게시글을 쓴 사람, 게시글 제목, 게시글 쓴 사람의 아이디를 봅니다.
    - 쿼리 파라미터 page를 통해 한 페이지에 5개씩 글 목록이 보입니다.
    - post_id를 패스파라미터로 받아 각 게시글의 세부 내용을 볼 수 있게 하였습니다.
    - id 0을 값을 가지는 포스트는 없으므로 posts_id 0을 전체 페이지로 구현했습니다.

>- #### 글 수정
    - method : **put**
    - http://127.0.0.1:8000/posts/read/<int:posts_id>
       ```
        body : {
                    "title":"수정!",
                    "content":"수정 내용"
                }
        ```
    - success response : {"message": "UPDATED!"}
    - 프론트가 put요청으로 body값에 title과 content를 값을 보내면 게시글이 수정되도록 하였습니다.
    - login_decorator를 이용하여 글을 작성한 유저만 글을 수정할 수 있게 하였습니다.

>- #### 글 삭제
    - method : **delete**
    - http://127.0.0.1:8000/posts/read/<int:posts_id>
    - success response : {"message":"DELETED!"}
    - 프론트가 delete요청을 보내면 그 글이 사라지게 만들었습니다.
    - login_decorator를 이용하여 글을 작성한 유저만 글을 삭제할 수 있게 하였습니다.