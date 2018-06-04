create table member(
	m_name text,
	m_username text unique not null,
	m_password text not null,
	m_location text,
	birthdate text ,
	phone_number integer,
	email text,
	bio text,
	profile_picture blob,
	agreement integer,
	m_follower text,
	m_following text,
	primary key(m_username)
);
create table posts(
	m_name text,
	m_username text unique not null,
	post text,
	postdate text,
	posttime text,
	likes integer,
	foreign key(m_name) references member,
	primary key(postdate,posttime)
);
