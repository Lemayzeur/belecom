**users**
	id [(pk) auto_increment]
	----
	email _[(varchar, maxlength=150, not null)]_
	first_name _[(varchar, maxlength=150)]_
	last_name [(varchar, maxlength=150)]
	password [(varchar, maxlength=100, not null)]
	photo [(varchar, maxlength=200)]

**products**
	id (pk) auto_increment
	-----
	name = varchar, max: 200, not null
	description = text , max 1000, not null
	category_id (fk, reference **categories**(id) restrict)
	old_price = [decimal]
	price = [decimal, not null]
	photo = [varchar,max:200 not null]

**categories**:
	id (pk) auto_increment
	----
	name [varchar, max: 100, not null]
	photo [varchar,max:200]

**stocks**:
	id (pk)
	----
	product_id [(fk) references **products**(id) on delete cascade]
	quantity = [int, default: 1]

**orders**
	id (pk) autoincrement
	----
	user_id (fk) references **users**(id) on delete restrict 
	sub_total: [dec, default=0, not null]
	discount:  [dec, default=0, not null]
	tax:  [dec, default=0, not null]
	total:  [dec, default=0, not null]

**order_products**
	id (pk) autoincrement
	----
	order_id (fk) references **orders**(id) on delete cascade 
	product_id (fk) references **products**(id) on delete cascade 
	price:  [dec]
	quantity: [dec, default=1]

**carts**:
	id (pk) auto_increment
	----
	user_id (fk) references **users**(id) on delete cascade 
	total [dec, default=0]

**cart_products**
	id (pk) auto_increment
	----
	cart_id (fk) references **carts**(id) on delete cascade 
	product_id (fk) references **products**(id) on delete cascade 
	price:  [dec]
	quantity: [dec, default=1]


**payments**
	id (pk)
	---
	user_id (fk) references **users**(id) on delete restrict 
	order_id (fk) references **orders**(id) on delete restrict 
	total_to_pay  [dec, not null]
	cash  [dec, not null]
	discount  [dec, default=0, not null]
	tax  [dec]
	return  [dec]
	payment_type (fk) references **payment_types** (id) on delete null

**payment_types**
	id (pk) auto_increment
	category = [varchar, max: 30, not null]
