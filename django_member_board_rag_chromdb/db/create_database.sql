-- root 또는 CREATE USER/GRANT 권한이 있는 MySQL 계정으로 실행합니다.
-- 실습용 데이터베이스(shopdb)가 이미 존재하면 삭제하지 않고 그대로 사용합니다.
CREATE DATABASE IF NOT EXISTS shopdb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- localhost에서 접속하는 Django 전용 계정을 생성합니다 (비밀번호: changeapp1234).
CREATE USER IF NOT EXISTS 'shopuser'@'localhost' IDENTIFIED BY 'changeapp1234';

-- 127.0.0.1로 접속하는 환경도 고려하여 동일 사용자 계정을 생성합니다.
CREATE USER IF NOT EXISTS 'shopuser'@'127.0.0.1' IDENTIFIED BY 'changeapp1234';

-- Docker 컨테이너 외부/내부 어디서든 접속할 수 있도록 와일드카드(%) 계정도 함께 생성합니다.
CREATE USER IF NOT EXISTS 'shopuser'@'%' IDENTIFIED BY 'changeapp1234';

-- shopdb의 모든 테이블에 대한 권한을 각 접속 호스트 계정에 부여합니다.
GRANT ALL PRIVILEGES ON shopdb.* TO 'shopuser'@'localhost';
GRANT ALL PRIVILEGES ON shopdb.* TO 'shopuser'@'127.0.0.1';
GRANT ALL PRIVILEGES ON shopdb.* TO 'shopuser'@'%';
GRANT ALL PRIVILEGES ON `test_%`.* TO 'shopuser'@'%';

-- 권한 변경 내용을 즉시 반영합니다.
FLUSH PRIVILEGES;