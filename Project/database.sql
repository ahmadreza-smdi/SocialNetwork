create table member(
	m_name varchar[20],
	m_username varchar[15] unique not null,
	m_password varchar[15] not null,
	m_location varchar[15],
	birthdate date ,
	phone_number varchar[15],
	email varchar[20],
	bio varchar[100],
	profile_picture blob,
	agreement bool,
	m_follower varchar[15],
	m_following varchar[15],
	primary key(m_username)
)

create table posts(
	m_name varchar[20],
	m_username varchar[15] unique not null,
	post varchar[140],
	postdate date,
	posttime time,
	likes number
	foreign key(m_name) references member,
	primary key(postdate,posttime)
)
