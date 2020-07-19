CREATE TABLE Business(
	bid char(7) not null,
	bname varchar(30) ,
	btype varchar(10) ,
	year integer,
	PRIMARY KEY (bid)
);
CREATE TABLE Objective(
	bid char(7) not null, 
	oid char(7) not null,
	content varchar(100),
	type varchar(10), 
	priority varchar(10),
	-- priority integer,
	PRIMARY KEY (bid,oid), 
	FOREIGN KEY (bid) REFERENCES Business
);