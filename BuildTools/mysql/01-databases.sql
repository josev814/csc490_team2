CREATE DATABASE IF NOT EXISTS test_stocksapp;

GRANT ALL PRIVILEGES ON test_stocksapp.* TO 'team2'@'%';
GRANT RELOAD ON *.* TO 'team2'@'%';