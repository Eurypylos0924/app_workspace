-- pytest creates and drops test_shopdb by itself, so shopuser needs rights on it.
-- Run ONCE as MySQL root (shopuser only has rights on shopdb by default).
GRANT ALL PRIVILEGES ON test_shopdb.* TO 'shopuser'@'%';
FLUSH PRIVILEGES;
