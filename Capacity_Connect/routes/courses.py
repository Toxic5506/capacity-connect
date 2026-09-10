from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models import db, User, Course, Enrollment, Assessment, Resource, Feedback
from routes.auth import login_required, role_required

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('')
def list_courses():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    level = request.args.get('level', '').strip()

    query = Course.query
    if search:
        query = query.filter((Course.title.ilike(f"%{search}%")) | (Course.description.ilike(f"%{search}%")))
    if category and category != 'All':
        query = query.filter_by(category=category)
    if level and level != 'All':
        query = query.filter_by(level=level)

    all_courses = query.order_by(Course.created_at.desc()).all()

    user_id = session.get('user_id')
    enrolled_course_ids = set()
    if user_id:
        enrolled = Enrollment.query.filter_by(user_id=user_id).all()
        enrolled_course_ids = {e.course_id for e in enrolled}

    categories = db.session.query(Course.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template('courses/index.html',
                           courses=all_courses,
                           enrolled_ids=enrolled_course_ids,
                           categories=categories,
                           selected_cat=category,
                           selected_level=level,
                           search=search)

@courses_bp.route('/<int:course_id>')
def course_detail(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        abort(404)

    user_id = session.get('user_id')
    enrollment = None
    user_feedback = None
    if user_id:
        enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course.id).first()
        user_feedback = Feedback.query.filter_by(user_id=user_id, course_id=course.id).first()

    assessments = Assessment.query.filter_by(course_id=course.id, is_active=True).all()
    resources = Resource.query.filter_by(course_id=course.id).all()
    feedbacks = Feedback.query.filter_by(course_id=course.id).order_by(Feedback.created_at.desc()).all()

    return render_template('courses/detail.html',
                           course=course,
                           enrollment=enrollment,
                           assessments=assessments,
                           resources=resources,
                           feedbacks=feedbacks,
                           user_feedback=user_feedback)

@courses_bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        abort(404)

    user_id = session['user_id']
    existing = Enrollment.query.filter_by(user_id=user_id, course_id=course.id).first()
    if not existing:
        new_enrollment = Enrollment(user_id=user_id, course_id=course.id, progress=15)
        db.session.add(new_enrollment)
        db.session.commit()
        flash(f'You have successfully enrolled in "{course.title}"!', 'success')
    else:
        flash('You are already enrolled in this course.', 'info')
    return redirect(url_for('courses.course_detail', course_id=course.id))

@courses_bp.route('/<int:course_id>/feedback', methods=['POST'])
@login_required
def submit_course_feedback(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        abort(404)

    user_id = session['user_id']
    rating = int(request.form.get('rating', 5))
    comments = request.form.get('comments', '').strip()

    fb = Feedback.query.filter_by(user_id=user_id, course_id=course.id).first()
    if fb:
        fb.rating = rating
        fb.comments = comments
        fb.created_at = datetime.now(timezone.utc)
        flash('Your feedback review has been updated.', 'success')
    else:
        fb = Feedback(course_id=course.id, user_id=user_id, rating=rating, comments=comments)
        db.session.add(fb)
        flash('Thank you for providing your feedback!', 'success')

    db.session.commit()
    return redirect(url_for('courses.course_detail', course_id=course.id))

@courses_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'trainer'])
def create_course():
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Technology').strip()
        level = request.form.get('level', 'Beginner').strip()
        duration = request.form.get('duration', '4 Weeks').strip()
        syllabus = request.form.get('syllabus', '').strip()
        thumbnail_url = request.form.get('thumbnail_url', '').strip()
        trainer_id = request.form.get('trainer_id', type=int) or session['user_id']
        is_featured = bool(request.form.get('is_featured'))

        if not code or not title or not description:
            flash('Please fill in code, title, and description.', 'error')
            return render_template('courses/create_edit.html', is_edit=False)

        if Course.query.filter_by(code=code).first():
            flash(f'Course code {code} already exists.', 'error')
            return render_template('courses/create_edit.html', is_edit=False)

        if not thumbnail_url:
            thumbnail_url = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=600&q=80"

        course = Course(
            code=code,
            title=title,
            description=description,
            category=category,
            level=level,
            duration=duration,
            syllabus=syllabus,
            thumbnail_url=thumbnail_url,
            trainer_id=trainer_id,
            is_featured=is_featured
        )
        db.session.add(course)
        db.session.commit()
        flash(f'Course "{title}" has been published successfully!', 'success')
        return redirect(url_for('courses.course_detail', course_id=course.id))

    trainers = User.query.filter(User.role.in_(['trainer', 'admin'])).all()
    return render_template('courses/create_edit.html', is_edit=False, trainers=trainers)
