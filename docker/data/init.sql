USE mydb;
GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'%';
FLUSH PRIVILEGE;

CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username TEXT,
    password TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    email TEXT NOT NULL
);


CREATE TABLE POSTS (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    username TEXT,
    title TEXT,
    content TEXT,
    views INTEGER DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

INSERT INTO USERS (username, password, email) VALUES
('user_kr1', 'password123', 'user_kr1@example.com'),
('user_kr2', 'password123', 'user_kr2@example.com'),
('user_kr3', 'password123', 'user_kr3@example.com'),
('user_int1', 'password123', 'user_int1@example.com'),
('user_int2', 'password123', 'user_int2@example.com'),
('user_int3', 'password123', 'user_int3@example.com');


INSERT INTO POSTS (username, title, content) VALUES
('user_kr1', '첫 번째 게시글 ✨', '환영합니다! 🥵'),
('user_kr1', '두 번째 게시글 ✨', '오늘도 좋은 하루! 🥵'),
('user_kr2', '세 번째 게시글 ✨', '여기는 어떻게 사용하나요? 🥵'),
('user_kr2', '네 번째 게시글 ✨', '점심 메뉴 추천 부탁드립니다 🥵'),
('user_kr3', '다섯 번째 게시글 ✨', '좋은 정보 감사합니다 🥵'),
('user_kr3', '여섯 번째 게시글 ✨', '주말 계획은 무엇인가요? 🥵'),
('user_int1', '일곱 번째 게시글 ✨', 'First post in this forum 🥵'),
('user_int1', '여덟 번째 게시글 ✨', 'How do you like it here? 🥵'),
('user_int2', '아홉 번째 게시글 ✨', 'Looking for movie recommendations 🥵'),
('user_int3', '열 번째 게시글 ✨', 'What is the weather like today? 🥵');