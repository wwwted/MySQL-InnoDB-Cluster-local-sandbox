mysql -uroot -proot -h127.0.0.1 -P3310 -se"select @@port\G select count(*) from test.employees"
mysql -uroot -proot -h127.0.0.1 -P3320 -se"select @@port\G select count(*) from test.employees"
mysql -uroot -proot -h127.0.0.1 -P3330 -se"select @@port\G select count(*) from test.employees"
