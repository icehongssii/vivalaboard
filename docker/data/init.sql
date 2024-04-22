CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` text,
  `password` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  `email` text NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `POSTS` (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `views` int DEFAULT '0',
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `POSTS_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `refresh_tokens` (
  `token_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `revoked` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`token_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `refresh_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



INSERT INTO POSTS (user_id, title, content, created_at, updated_at, views) VALUES
(9, '질문 ddd하고싶어asdasdasd~~ 깔깔', 'Jam$e11s1ddddddddding12 ?3', '2024-04-23 05:25:55', '2024-04-23 05:25:55', 0),
(9, '질문 ddd하고싶어asdasdasd~~ 깔깔', 'Jam$e11s1ddddddddding12 ?3', '2024-04-23 05:25:57', '2024-04-23 05:25:57', 0),
(9, '질문 ddd하고싶어asdasdasd~~ 깔깔', 'Jam$e11s1ddddddddding12 ?3', '2024-04-23 05:25:58', '2024-04-23 05:25:58', 0);


INSERT INTO USERS (user_id, username, password, created_at, updated_at, email) VALUES
(7, 'jeil', '$2b$12$p5nsUTGKzc67vG7vx52qoeHPLxAVEft0O3LlzEMmUiSEikGufbJyy', '2024-04-22 20:24:14', '2024-04-22 20:24:14', 'jeil3133ddd3d3@naver.com'),
(8, 'jeil', '$2b$12$r3Ukee4uujo/RIfXnOuBAuAn3LnyOWbavMYkhPsVW6NlncLfZ1wcS', '2024-04-22 20:24:28', '2024-04-22 20:24:28', 'jeil31dasdasd33ddd3d3@naver.com'),
(9, '??!!', '$2b$12$GWQovRukkvRk9skJ2RPsbOuGgDXYlO2rDIPwX0.VseM2YjHOiUwiS', '2024-04-22 20:24:35', '2024-04-22 20:24:35', 'jeil31dasdasdddd33ddd3d3@naver.com');

INSERT INTO refresh_tokens (token_id, user_id, token, expires_at, created_at, updated_at, revoked) VALUES
(31, 9, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5IiwiaWF0IjoxNzEzODE3NDkzLCJleHAiOjE3MTM5MDM4OTMsImlzcyI6InZpdmFsYWJvYXJkIn0.ZQakoXrg_qXVeCxgz5DC8x8SUwB4uvXSJgvNwn7HtX0', '2024-04-24 05:24:54', '2024-04-23 05:24:54', '2024-04-22 20:24:53', 0);
