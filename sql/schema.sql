DROP TABLE IF EXISTS order_reviews CASCADE;
DROP TABLE IF EXISTS order_payments CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS sellers CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS geolocation CASCADE;

CREATE TABLE geolocation (
    zip_code_prefix     INTEGER PRIMARY KEY,
    lat                 DECIMAL(9,6) NOT NULL,
    lng                 DECIMAL(9,6) NOT NULL,
    city                VARCHAR(100) NOT NULL,
    state               CHAR(2) NOT NULL
);

CREATE TABLE customers (
    customer_id         VARCHAR(32) PRIMARY KEY,
    customer_unique_id  VARCHAR(32) NOT NULL,
    zip_code_prefix     INTEGER NOT NULL,
    city                VARCHAR(100) NOT NULL,
    state               CHAR(2) NOT NULL
);

CREATE TABLE sellers (
    seller_id           VARCHAR(32) PRIMARY KEY,
    zip_code_prefix     INTEGER NOT NULL,
    city                VARCHAR(100) NOT NULL,
    state               CHAR(2) NOT NULL
);

CREATE TABLE products (
    product_id              VARCHAR(32) PRIMARY KEY,
    category_name           VARCHAR(100) NOT NULL,
    category_name_english   VARCHAR(100),
    name_length             SMALLINT,
    description_length      INTEGER,
    photos_qty              SMALLINT,
    weight_g                REAL,
    length_cm               REAL,
    height_cm               REAL,
    width_cm                REAL
);

CREATE TABLE orders (
    order_id                    VARCHAR(32) PRIMARY KEY,
    customer_id                 VARCHAR(32) NOT NULL,
    status                      VARCHAR(20) NOT NULL,
    purchase_timestamp          TIMESTAMP NOT NULL,
    approved_at                 TIMESTAMP,
    delivered_carrier_date      TIMESTAMP,
    delivered_customer_date     TIMESTAMP,
    estimated_delivery_date     DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id            VARCHAR(32) NOT NULL,
    order_item_id       SMALLINT NOT NULL,
    product_id          VARCHAR(32) NOT NULL,
    seller_id           VARCHAR(32) NOT NULL,
    shipping_limit_date TIMESTAMP NOT NULL,
    price               DECIMAL(10,2) NOT NULL,
    freight_value       DECIMAL(10,2),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

CREATE TABLE order_payments (
    order_id                VARCHAR(32) NOT NULL,
    payment_sequential      SMALLINT NOT NULL,
    payment_type            VARCHAR(20) NOT NULL,
    payment_installments    SMALLINT NOT NULL,
    payment_value           DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_reviews (
    review_id               VARCHAR(32) NOT NULL,
    order_id                VARCHAR(32) NOT NULL,
    review_score            SMALLINT NOT NULL CHECK (review_score BETWEEN 1 AND 5),
    comment_title           TEXT,
    comment_message         TEXT,
    creation_date           DATE NOT NULL,
    answer_timestamp        TIMESTAMP,
    PRIMARY KEY (review_id, order_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_purchase ON orders(purchase_timestamp);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_order_items_seller ON order_items(seller_id);
CREATE INDEX idx_customers_state ON customers(state);
CREATE INDEX idx_sellers_state ON sellers(state);
CREATE INDEX idx_products_category ON products(category_name);
CREATE INDEX idx_reviews_score ON order_reviews(review_score);
