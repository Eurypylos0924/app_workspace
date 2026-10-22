-- 주의: sql 폴더의 파일은 모두 첫 시작 때 자동 실행되므로 이 파일도 한 번 실행됩니다.
-- (그래서 마우스 재고가 29로 시작합니다.) 실습은 mysql 접속 후 한 줄씩 직접 실행해 보세요.
-- 접속: docker exec -it chapter07-mysql mysql -u shopuser -p shopdb

-- 조회: 가격이 비싼 순서로 전체 상품을 봅니다.
SELECT id, name, price, stock FROM practice_products ORDER BY price DESC;

-- 조건 조회: 가격이 10만 원보다 싼 상품만 봅니다.
SELECT name, price FROM practice_products WHERE price < 100000;

-- 추가: 새 상품을 넣습니다.
INSERT INTO practice_products (name, price, stock) VALUES ('모니터', 220000, 8);

-- 수정: 이름이 '마우스'인 상품의 재고를 1 줄입니다. (재고가 있을 때만)
UPDATE practice_products SET stock = stock - 1 WHERE name = '마우스' AND stock > 0;

-- 삭제: 이름이 '모니터'인 상품을 지웁니다.
DELETE FROM practice_products WHERE name = '모니터';

-- 집계: 상품 개수와 전체 재고 합계를 봅니다.
SELECT COUNT(*) AS product_count, SUM(stock) AS total_stock FROM practice_products;
