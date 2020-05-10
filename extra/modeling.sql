PRAGMA foreign_keys = ON; -- Enable foreign keys
PRAGMA count_changes = True;

CREATE TABLE IF NOT EXISTS user (
	user_name VARCHAR(255),
	user_key VARCHAR(255) NOT NULL,
	user_format_short VARCHAR(255) NOT NULL,
	user_expiration CHAR NOT NULL,
	user_avatar_url VARCHAR(255) NOT NULL,
	user_private INT NOT NULL,
	user_website VARCHAR(255),
	user_email VARCHAR(255) NOT NULL,
	user_location VARCHAR(255),
	user_account_type INT NOT NULL,

	CONSTRAINT pk_user PRIMARY KEY(user_name)
);

CREATE TABLE IF NOT EXISTS paste_info (
	paste_key VARCHAR(255),
	owner VARCHAR(255) NOT NULL,
	paste_date INT NOT NULL,
	paste_title VARCHAR(255),
	paste_size INT NOT NULL,
	paste_expire_date INT NOT NULL,
	paste_private INT NOT NULL,
	paste_format_long VARCHAR(255) NOT NULL,
	paste_format_short VARCHAR(255) NOT NULL,
	paste_url VARCHAR(255) NOT NULL,
	paste_hits INT NOT NULL,

	CONSTRAINT pk_paste PRIMARY KEY(paste_key),
	CONSTRAINT fk_paste_owner FOREIGN KEY(owner)
		REFERENCES user(user_name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paste_text (
	paste_key VARCHAR(255),
	paste BLOB NOT NULL,

	CONSTRAINT uk_paste_text UNIQUE(paste_key),
	CONSTRAINT fk_paste_text FOREIGN KEY(paste_key)
		REFERENCES paste_info(paste_key) ON DELETE CASCADE
);
