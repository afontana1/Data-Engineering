from flask import render_template, request, redirect, url_for
from sqlalchemy import or_

from app import app
from app import db
from models.course import Course


@app.route("/courses")
def courses():
    search_query = request.args.get("search", "")

    if search_query:
        # Query the database for courses matching the search query
        course_recs = (
            db.session.query(Course)
            .filter(or_(Course.course_name.ilike(f"%{search_query}%")))
            .all()
        )
    else:
        # Query the database for all courses
        course_recs = db.session.query(Course).all()

    courses = list(map(lambda rec: rec.__dict__, course_recs))

    return render_template("courses.html", courses=courses)


@app.route("/course", methods=["GET", "POST"])
def course():
    course_id = request.args.get("course_id")
    if request.method == "GET":
        if course_id:
            course = Course.query.get(course_id)
            if not course:
                app.logger.error(f"Course with id {course_id} not found...")
                return redirect(url_for("courses"))
            form_action = request.args.get("action")
            if form_action == "edit":
                return render_template("course_form.html", course=course)
            elif form_action == "delete":
                db.session.delete(course)
                db.session.commit()
                return redirect(url_for("courses"))
            return render_template("course_detail.html", course=course)
        else:
            return render_template("course_form.html", course=None)
    elif request.method == "POST":
        course_id = request.form["course_id"]
        course_name = request.form["course_name"]
        course_author = request.form["course_author"]
        course_endpoint = request.form["course_endpoint"]
        if course_id:
            course = Course.query.get(course_id)
            course.course_name = course_name
            course.course_author = course_author
            course.course_endpoint = course_endpoint
        else:
            course = Course(
                course_name=course_name,
                course_author=course_author,
                course_endpoint=course_endpoint,
            )
            db.session.add(course)
        db.session.commit()
        return redirect(url_for("courses"))
