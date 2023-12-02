from flask import Flask, request, render_template, redirect, session
import pymysql
from datetime import datetime, timedelta
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static/categories"


app = Flask(__name__)
app.secret_key = 'kutty'
conn = pymysql.connect(host="localhost", user="root", password="root", db="jobRecruitment")
cursor = conn.cursor()


admin_username = "admin"
admin_password = "admin"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == admin_username and password == admin_password:
        session['role'] = 'admin'
        return redirect("/admin_home")
    else:
        return render_template("msg.html", message="invalid login details")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/view_recruiter")
def view_recruiter():
    cursor.execute("select * from recruiters")
    recruiters = cursor.fetchall()
    return render_template("view_recruiter.html", recruiters=recruiters)


@app.route("/verify_recruiter")
def verify_recruiter():
    recruiter_id = request.args.get("recruiter_id")
    cursor.execute("update recruiters set status = 'verified' where recruiter_id = '" + str(recruiter_id) + "'")
    conn.commit()
    return redirect("/view_recruiter")


@app.route("/add_categories")
def add_categories():
    cursor.execute("select * from categories")
    categories = cursor.fetchall()
    return render_template("add_categories.html", categories=categories)


@app.route("/add_categories_action",methods=['post'])
def add_categories_action():
    category_name = request.form.get("category_name")
    picture = request.files.get("picture")
    picture_name = picture.filename
    path = APP_ROOT + "/" + picture_name
    picture.save(path)
    count = cursor.execute(" select * from categories where category_name='"+str(category_name)+"' ")
    if count > 0:
        return render_template("msg.html", message="Duplicate entry")
    else:
        cursor.execute("insert into categories(category_name,picture) values('" + str(category_name) + "','" + str(picture.filename) + "')")
        conn.commit()
        return render_template("msg.html", message="Categories added successfully")


@app.route("/add_subcategories")
def add_subcategories():
    cursor.execute("select * from categories")
    categories = cursor.fetchall()
    return render_template("add_subcategories.html", categories=categories, get_categories_by_category_id = get_categories_by_category_id)


def get_categories_by_category_id(category_id):
    cursor.execute("select * from categories where category_id ='"+str(category_id)+"' ")
    categories = cursor.fetchall()
    return categories[0]


@app.route("/add_subcategories_action", methods=['post'])
def add_subcategories_action():
    category_id = request.form.get("category_id")
    subCategory_name = request.form.get("subCategory_name")
    picture = request.files.get("picture")
    picture_name = picture.filename
    path = APP_ROOT + "/" + picture_name
    picture.save(path)
    count =cursor.execute("select * from subcategories where subCategory_name='"+str(subCategory_name)+"' and category_id='"+str(category_id)+"'")
    if count > 0:
        return render_template("msg.html", message="Duplicate subcategory name")
    else:
        cursor.execute("insert into subcategories(category_id,subCategory_name,picture) values('"+str(category_id)+"','"+str(subCategory_name)+"','"+str(picture.filename)+"')")
        conn.commit()
        return render_template("msg.html", message="subCategory added successfully")


@app.route("/get_subcategories")
def get_subcategories():
    category_id = request.args.get("category_id")
    if category_id == "":
        query = "select * from subcategories"
    else:
        query = "select * from subcategories where category_id='" + str(category_id) + "'"
    cursor.execute(query)
    subcategories = cursor.fetchall()
    print(subcategories)
    return render_template("get_subcategories.html", subcategories=subcategories, get_categories_by_category_id=get_categories_by_category_id)


@app.route("/recruiter_login")
def recruiter_login():
    return render_template("recruiter_login.html")


@app.route("/recruiter_login_action", methods=['post'])
def recruiter_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from recruiters where email='" + str(email) + "' and password='" + str(password) + "' ")
    if count > 0:
        recruiters = cursor.fetchall()
        status = recruiters[0][7]
        if status == 'verified':
            session['recruiter_id'] = recruiters[0][0]
            session['role'] = 'recruiter'
            return redirect("/recruiter_home")
        else:
            return render_template("msg.html", message=" Your account is Not Verified")
    else:
        return render_template("msg.html", message="Invalid Login Details")


@app.route("/recruiter_home")
def recruiter_home():
    return render_template("recruiter_home.html")


@app.route("/recruiter_registration")
def recruiter_registration():
    return render_template("recruiter_registration.html")


@app.route("/recruiter_registration_action", methods=['post'])
def recruiter_registration_action():
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")
    gender = request.form.get("gender")
    age = request.form.get("age")
    status = 'not verified'
    company_name = request.form.get("company_name")
    cursor.execute("insert into recruiters(name, phone, email, password, gender, age, status, company_name) values('" + str(name) + "','" + str(phone) + "','" + str(email) + "','" + str(password) + "','" + str(gender) + "','" + str(age) + "','" + str(status) + "','" + str(company_name) + "')")
    conn.commit()
    return render_template("msg.html", message="recruiter registered successfully")


@app.route("/post_job_recruitments")
def post_job_recruitments():
    cursor.execute("select * from subcategories")
    subcategories = cursor.fetchall()
    return render_template("post_job_recruitments.html", subcategories=subcategories, get_subcategories_by_subCatogory_id = get_subcategories_by_subCategory_id, get_subcategories_by_category_id = get_subcategories_by_category_id)


def get_subcategories_by_subCategory_id(subCategory_id):
    cursor.execute("select * from subcategories where subCategory_id ='"+str(subCategory_id)+"' ")
    subcategories = cursor.fetchall()
    return subcategories[0]


def get_subcategories_by_category_id(category_id):
    cursor.execute("select * from subcategories where category_id = '"+str(category_id)+"' ")
    subcategories = cursor.fetchall()
    return subcategories[0]


@app.route("/post_job_recruitments_action", methods=['post'])
def post_job_recruitments_action():
    recruiter_id = session['recruiter_id']
    subCategory_id = request.form.get("subCategory_id")
    print(subCategory_id)
    job_title = request.form.get("job_title")
    description = request.form.get("description")
    experience = request.form.get("experience")
    number_of_openings = request.form.get("number_of_openings")
    skills = request.form.get("skills")
    package = request.form.get("package")
    job_location = request.form.get("job_location")
    working_hours = request.form.get("working_hours")
    company_profile = request.form.get("company_profile")
    cursor.execute("insert into job_recruitments(recruiter_id,subCategory_id, job_title, description, experience, number_of_openings,skills,company_profile,package,job_location,working_hours) values('"+str(recruiter_id)+"','"+str(subCategory_id)+"','"+str(job_title)+"','"+str(description)+"','"+str(experience)+"','"+str(number_of_openings)+"','"+str(skills)+"','"+str(company_profile)+"','"+str(package)+"','"+str(job_location)+"','"+str(working_hours)+"')")
    conn.commit()
    return render_template("msg.html", message=" Job Recruitments added successfully")


@app.route("/view_post_job_recruitments")
def view_post_job_recruitments():
    cursor.execute("select * from job_recruitments")
    job_recruitments = cursor.fetchall()
    return render_template("view_post_job_recruitments.html", job_recruitments=job_recruitments,get_subcategories_by_subCategory_id=get_subcategories_by_subCategory_id ,get_subcategories_by_category_id=get_subcategories_by_category_id)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/job_seeker_login")
def job_seeker_login():
    return render_template("job_seeker_login.html")


@app.route("/job_seeker_login_action", methods=['post'])
def job_seeker_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from job_seekers where email='" + str(email) + "' and password='" + str(password) + "' ")
    if count > 0:
        job_seekers = cursor.fetchall()
        session['job_seeker_id'] = job_seekers[0][0]
        session['role'] = 'job_seeker'
        return redirect("/job_seeker_home")
    else:
        return render_template("msg.html", message="invalid login details")


@app.route("/job_seeker_home")
def job_seeker_home():
    job_seeker_id = session['job_seeker_id']
    cursor.execute("select * from job_seekers where job_seeker_id='"+str(job_seeker_id)+"'")
    job_seekers = cursor.fetchall()
    return render_template("job_seeker_home.html",job_seekers=job_seekers)


@app.route("/job_seeker_registration")
def job_seeker_registration():
    return render_template("job_seeker_registration.html")


@app.route("/job_seeker_registration_action", methods=['post'])
def job_seeker_registration_action():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    gender = request.form.get("gender")
    age = request.form.get("age")
    qualification = request.form.get("qualification")
    experience = request.form.get("experience")
    resume = request.files.get("resume")
    resume_name = resume.filename
    path = APP_ROOT + "/" + resume_name
    resume.save(path)
    cursor.execute("insert into job_seekers(name,email,phone,password,gender,age,qualification,experience,resume) values('" + str(name) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "','" + str(gender) + "','" + str(age) + "','" + str(qualification) + "','" + str(experience) + "','" + str(resume.filename) + "')")
    conn.commit()
    return render_template("msg.html", message="Job Seeker login successfully")


@app.route("/add_certifications")
def add_certifications():
    return render_template("add_certifications.html")


@app.route("/add_certifications_action",methods=['post'])
def add_certifications_action():
    job_seeker_id = session['job_seeker_id']
    certification_title = request.form.get("certification_title")
    certification = request.form.get("certification")
    cursor.execute("insert into certifications(job_seeker_id,certification_title,certification) values('"+str(job_seeker_id)+"','"+str(certification_title)+"','"+str(certification)+"')")
    conn.commit()
    return render_template("msg.html", message="Certificate added successfully")


@app.route("/view_certifications")
def view_certifications():
    cursor.execute("select * from certifications")
    certifications = cursor.fetchall()
    return render_template("view_certifications.html",certifications=certifications)


@app.route("/add_qualifications")
def add_qualifications():
    return render_template("add_qualifications.html")


@app.route("/add_qualifications_action",methods=['post'])
def add_qualifications_action():
    job_seeker_id = session['job_seeker_id']
    year_of_passedOut = request.form.get("year_of_passedOut")
    percentage = request.form.get("percentage")
    cursor.execute("insert into qualifications(job_seeker_id,year_of_passedOut,percentage) values('"+str(job_seeker_id)+"','"+str(year_of_passedOut)+"','"+str(percentage)+"')")
    conn.commit()
    return render_template("msg.html", message="Qualifications added successfully")


@app.route("/view_qualifications")
def view_qualifications():
    cursor.execute("select * from qualifications")
    qualifications = cursor.fetchall()
    return render_template("view_qualifications.html",qualifications=qualifications)


@app.route("/search_job_recruitment")
def search_job_recruitment():
    cursor.execute("select * from job_recruitments")
    job_recruitments = cursor.fetchall()
    cursor.execute("SELECT DISTINCT(job_title) FROM job_recruitments")
    job_title = cursor.fetchall()
    return render_template("search_job_recruitment.html",job_recruitments=job_recruitments,job_title=job_title)


@app.route("/get_job_recruitments")
def get_job_recruitments():
    job_title = request.args.get("job_title")
    cursor.execute("select * from job_recruitments where job_title like '%" + str(job_title) + "%' ")
    conn.commit()
    job_recruitments =cursor.fetchall()
    return render_template("get_job_recruitments.html",job_recruitments = job_recruitments)


@app.route("/apply_job")
def apply_job():
    job_seeker_id = session['job_seeker_id']
    job_recruitment_id = request.args.get("job_recruitment_id")
    status = request.args.get("status")
    cursor.execute("insert into job_applications(job_seeker_id,job_recruitment_id,status) values('"+str(job_seeker_id)+"','"+str(job_recruitment_id)+"','Applied')")
    conn.commit()
    job_applications = cursor.fetchall()
    cursor.execute("select * from job_Seekers where job_seeker_id='"+str(job_seeker_id)+"'")
    job_Seekers = cursor.fetchall()
    date = datetime.now().date()
    return render_template("msg.html",message="Job Applied successfully", job_Seekers=job_Seekers[0], date=date,job_applications=job_applications)


@app.route("/view_job_applications")
def view_job_applications():
    role = session['role']
    if role == 'job_seeker':
        job_seeker_id = session['job_seeker_id']
        query = "select * from job_applications where job_seeker_id='"+str(job_seeker_id)+"'"
    elif role == 'recruiter':
        job_recruitment_id = request.args.get("job_recruitment_id")
        query = "select * from job_applications where job_recruitment_id='" + str(job_recruitment_id) + "'"
    cursor.execute(query)
    job_applications = cursor.fetchall()
    job_applications = list(job_applications)
    job_applications.reverse()
    return render_template("view_job_applications.html", job_applications = job_applications, get_name_by_job_seeker_id=get_name_by_job_seeker_id, get_job_recruitments_by_job_recruitment_id=get_job_recruitments_by_job_recruitment_id, get_job_recruitment_id_by_recruiter_id=get_job_recruitment_id_by_recruiter_id)


def get_job_recruitment_id_by_recruiter_id(recruiter_id):
    cursor.execute("select job_recruitments  where job_recruitment_id in (select job_recruitment_id  where recruiter_id in(select recruiter_idfrom recruiters where  recruiter_id= '"+str(recruiter_id)+"'))")
    recruiters = cursor.fetchall()
    return recruiters[0]


def get_name_by_job_seeker_id(job_seeker_id):
    cursor.execute("select * from job_seekers where job_seeker_id='"+str(job_seeker_id)+"'")
    job_seekers = cursor.fetchall()
    return job_seekers[0]


def get_job_recruitments_by_job_recruitment_id(job_recruitment_id):
    cursor.execute("select * from job_recruitments where job_recruitment_id='"+str(job_recruitment_id)+"'")
    job_recruitments = cursor.fetchall()
    return job_recruitments[0]


@app.route("/accept_application", methods=['get'])
def accept_application():
    job_application_id = request.args.get("job_application_id")
    cursor.execute(" update job_applications set status = 'Accepted' where job_application_id='"+str(job_application_id)+"' ")
    conn.commit()
    return render_template("msg.html", message="Application accepted")


@app.route("/reject_application", methods=['get'])
def reject_application():
    job_application_id = request.args.get("job_application_id")
    cursor.execute(" update job_applications set status = 'Rejected' where job_application_id='"+str(job_application_id)+"' ")
    conn.commit()
    return render_template("msg.html", message="Application Rejected")


@app.route("/schedule_interview",methods=['get'])
def schedule_interview():
    job_application_id = request.args.get("job_application_id")
    return render_template("schedule_interview.html", job_application_id=job_application_id)


@app.route("/schedule_interview_action",methods=['get'])
def schedule_interview_action():
    job_application_id = request.args.get("job_application_id")
    interview_type = request.args.get("interview_type")
    status = request.args.get("status")
    date_time = request.args.get("date_time")
    cursor.execute("insert into schedules(job_application_id,interview_type,date_time,status)  values('"+str(job_application_id)+"','"+str(interview_type)+"','"+str(date_time)+"','Scheduled')")
    conn.commit()
    cursor.execute("update job_applications set status = 'scheduled' where job_application_id='"+str(job_application_id)+"'")
    conn.commit()
    return render_template("msg.html", message="Scheduled Interview")


@app.route("/view_interview_schedule")
def view_interview_schedule():
    job_application_id = request.args.get("job_application_id")
    cursor.execute("select * from schedules where job_application_id='"+str(job_application_id)+"'")
    schedules = cursor.fetchall()
    return render_template("view_interview_schedule.html",schedules= schedules[0])


@app.route("/accept_interview",methods=['get'])
def accept_interview():
    schedule_id = request.args.get("schedule_id")
    cursor.execute(" update schedules set status = 'Accepted' where schedule_id='"+str(schedule_id)+"' ")
    conn.commit()
    return render_template("msg.html", message="Interview Accepted")


@app.route("/reject_interview",methods=['get'])
def reject_interview():
    schedule_id = request.args.get("schedule_id")
    cursor.execute(" update schedules set status = 'Rejected' where schedule_id='"+str(schedule_id)+"' ")
    conn.commit()
    return render_template("msg.html", message="Interview Rejected")


@app.route("/accept_candidate",methods=['get'])
def accept_candidate():
    schedule_id = request.args.get("schedule_id")
    cursor.execute(" update schedules set status = 'Accepted candidate' where schedule_id='"+str(schedule_id)+"' ")
    conn.commit()
    return render_template("msg.html", message="Candidate Accepted")


@app.route("/reject_candidate",methods=['get'])
def reject_candidate():
    schedule_id = request.args.get("schedule_id")
    cursor.execute(" update schedules set status = 'Rejected candidate' where schedule_id='"+str(schedule_id)+"' ")
    conn.commit()
    return render_template("msg.html", message="Candidate Rejected")



app.run(debug=True)