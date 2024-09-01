create database if not exists testdb;
use testdb;

DROP TABLE IF EXISTS ecommerce_transactions;
CREATE TABLE ecommerce_transactions (
    CustomerID STRING,
    ProductID STRING,
    Category STRING,
    Price DECIMAL(10,2),
    Quantity INT,
    TransactionDate TIMESTAMP,
    ReviewRating INT,
    ReviewText STRING,
    CustomerAge INT,
    CustomerGender STRING,
    Country STRING,
    DeviceType STRING,
    BrowsingDuration INT,
    PreviousPurchases INT
)

COMMENT 'Table storing e-commerce transaction data'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
LOAD DATA LOCAL INPATH '/data/ecommerce_transactions.csv' INTO TABLE ecommerce_transactions;


