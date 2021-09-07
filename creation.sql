create table Users (id integer Primary Key,
					username varchar(80) NOT NULL,
					first_name varchar(80),
					last_name varchar(80),
					is_admin bool NOT NULL DEFAULT false,
					created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP(0));

create table Orders (id varchar(32) Primary Key,
					start_point timestamptz NOT NULL,
					work_type varchar(80) NOT NULL,
					work_interval interval NOT NULL,
					user_id integer REFERENCES Users (id) NOT NULL,
					created_at TIMESTAMPTZ NOT NULL DEFAULT NOW());
					
create table WorkPeriods (id varchar(32) Primary Key,
						 work_date date NOT NULL,
						 start_point timestamptz NOT NULL,
						 end_point timestamptz NOT NULL);