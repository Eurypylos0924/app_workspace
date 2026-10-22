-- Docker가 처음 실행될 때 자동으로 실행되는 테이블 생성 SQL입니다.
-- Django ORM이 만드는 테이블(shop_product)과는 별개의 연습용 테이블입니다.
CREATE TABLE IF NOT EXISTS practice_products (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    CONSTRAINT chk_practice_price CHECK (price >= 0),
    CONSTRAINT chk_practice_stock CHECK (stock >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
