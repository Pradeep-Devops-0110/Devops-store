CREATE TABLE products(id SERIAL PRIMARY KEY,name TEXT NOT NULL,description TEXT NOT NULL,price_cents INTEGER NOT NULL,stock INTEGER NOT NULL DEFAULT 100);
CREATE TABLE orders(id UUID PRIMARY KEY,customer_email TEXT NOT NULL,total_cents INTEGER NOT NULL,status TEXT NOT NULL,payment_id TEXT,created_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE order_items(order_id UUID REFERENCES orders(id) ON DELETE CASCADE,product_id INTEGER,product_name TEXT,quantity INTEGER,unit_price_cents INTEGER,PRIMARY KEY(order_id,product_id));
INSERT INTO products(name,description,price_cents,stock) VALUES ('Everyday Backpack','Durable 20L backpack for work and travel.',4999,25),('Insulated Bottle','Reusable stainless steel bottle, 750 ml.',1899,40),('Desk Lamp','Dimmable LED lamp with warm light.',3299,15);
