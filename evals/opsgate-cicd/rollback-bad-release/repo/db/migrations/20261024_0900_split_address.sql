-- Added in v2.3.0
ALTER TABLE orders ADD COLUMN shipping_street text;
ALTER TABLE orders ADD COLUMN shipping_city text;
UPDATE orders SET shipping_street = split_part(shipping_address, ',', 1),
                  shipping_city = split_part(shipping_address, ',', 2);
ALTER TABLE orders DROP COLUMN shipping_address;
