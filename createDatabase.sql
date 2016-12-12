create table Sites (
	id INT NOT NULL AUTO_INCREMENT,
	sitename varchar(255),
	PRIMARY KEY (id)
);

create table Questions (
	id INT NOT NULL AUTO_INCREMENT,
	site_id INT,
	stackexchange_id INT NOT NULL,
	score INT,
	view_count INT,
	body BLOB,
	PRIMARY KEY (id),
	FOREIGN KEY (site_id)
		REFERENCES Sites(id)
		ON DELETE CASCADE
);

create table Answers (
	id INT NOT NULL AUTO_INCREMENT,
	question_id INT,
	stackexchange_id INT NOT NULL,
	score INT,
	body BLOB,
	entities INT,
	sentences INT,
	link_ratio REAL,
	tag_ratio REAL,
	similarity REAL,
	PRIMARY KEY (id),
	FOREIGN KEY (question_id)
		REFERENCES Questions(id)
		ON DELETE CASCADE
);
