create database jobRecruitment;
use jobRecruitment;
drop database jobRecruitment;

create table recruiters(
recruiter_id int auto_increment primary key,
name varchar(255) not null,
phone           varchar(255) not null unique,
email           varchar(255) not null unique,
password        varchar(255) not null,
gender          varchar(255) not null,
age             varchar(255) not null,
status          varchar(255) not null,
company_name   varchar(255) not null
);

create table categories(
category_id int auto_increment primary key,
category_name  varchar(255) not null,
picture        varchar(255) not null
);

create table subCategories(
subCategory_id int auto_increment primary key,
category_id int not null,
subCategory_name  varchar(255) not null,
picture           varchar(255) not null,
foreign key (category_id) references categories(category_id)
);

create table job_recruitments(
job_recruitment_id int auto_increment primary key,
recruiter_id int not null,
subCategory_id int not null,
job_title varchar(255) not null,
description varchar(255) not null,
experience varchar(255) not null,
number_of_openings varchar(255) not null,
skills varchar(255) not null,
company_profile varchar(255) not null,
package varchar(255) not null,
job_location varchar(255) not null,
working_hours varchar(255) not null,
foreign key (recruiter_id) references recruiters(recruiter_id),
foreign key (subCategory_id) references subCategories(subCategory_id)
);

create table job_seekers(
job_seeker_id int auto_increment primary key,
name            varchar(255) not null,
phone           varchar(255) not null unique,
email           varchar(255) not null unique,
password        varchar(255) not null,
gender          varchar(255) not null,
age             varchar(255) not null,
qualification   varchar(255) not null,
experience      varchar(255) not null,
resume          varchar(255) not null
);

create table qualifications(
qualification_id int auto_increment primary key,
job_seeker_id int not null,
year_of_passedOut varchar(255) not null,
percentage        varchar(255) not null,
foreign key (job_seeker_id) references job_seekers(job_seeker_id)
);

create table certifications(
certification_id int auto_increment primary key,
job_seeker_id int not null,
certification_title varchar(255) not null,
certification       varchar(255) not null,
foreign key (job_seeker_id) references job_seekers(job_seeker_id)
);


create table job_applications(
job_application_id int auto_increment primary key,
date datetime default current_timestamp,
status         varchar(255) not null,
job_recruitment_id int not null,
job_seeker_id int not null,
foreign key (job_recruitment_id) references job_recruitments(job_recruitment_id),
foreign key (job_seeker_id) references job_seekers(job_seeker_id)
);

create table schedules(
schedule_id int auto_increment primary key,
job_application_id int not null,
interview_type varchar(255) not null,
date_time varchar(255) not null,
status varchar(255) not null,
foreign key (job_application_id) references job_applications(job_application_id)
);