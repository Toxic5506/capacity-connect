import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, abort
from werkzeug.utils import secure_filename
from models import db, User, Course, Assessment, Question, Submission, Enrollment, Resource
from routes.auth import login_required, role_required

trainer_bp = Blueprint('trainer', __name__, url_prefix='/trainer')

@trainer_bp.route('/assessments/new', methods=['GET', 'POST'])
@login_required
@role_required(['trainer', 'admin'])
def create_assessment():
    user = db.session.get(User, session['user_id'])
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subject = request.form.get('subject', '').strip()
        description = request.form.get('description', '').strip()
        course_id = request.form.get('course_id', type=int)
        time_limit = int(request.form.get('time_limit_minutes', 15))
        passing_score = int(request.form.get('passing_score', 70))
        deadline_str = request.form.get('deadline', '')

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except Exception:
                pass

        if not title or not subject:
            flash('Please provide an assessment title and subject.', 'error')
            return render_template('assessments/manage.html', courses=Course.query.all())

        asm = Assessment(
            title=title,
            subject=subject,
            description=description,
            course_id=course_id if course_id else None,
            trainer_id=user.id,
            time_limit_minutes=time_limit,
            passing_score=passing_score,
            deadline=deadline,
            is_active=True
        )
        db.session.add(asm)
        db.session.flush()

        q_count = int(request.form.get('question_counter', 1))
        added_q = 0
        for i in range(1, q_count + 1):
            q_text = request.form.get(f'q_text_{i}', '').strip()
            opt_a = request.form.get(f'q_a_{i}', '').strip()
            opt_b = request.form.get(f'q_b_{i}', '').strip()
            opt_c = request.form.get(f'q_c_{i}', '').strip()
            opt_d = request.form.get(f'q_d_{i}', '').strip()
            correct = request.form.get(f'q_correct_{i}', 'A').strip().upper()
            explanation = request.form.get(f'q_expl_{i}', '').strip()

            if q_text and opt_a and opt_b:
                q = Question(
                    assessment_id=asm.id,
                    question_text=q_text,
                    option_a=opt_a,
                    option_b=opt_b,
                    option_c=opt_c or 'N/A',
                    option_d=opt_d or 'N/A',
                    correct_option=correct,
                    explanation=explanation
                )
                db.session.add(q)
                added_q += 1

        db.session.commit()
        flash(f'Assessment "{title}" created with {added_q} questions successfully!', 'success')
        return redirect(url_for('assessments.list_assessments'))

    courses = Course.query.all()
    return render_template('assessments/manage.html', courses=courses)

@trainer_bp.route('/trainees')
@login_required
@role_required(['trainer', 'admin'])
def trainer_trainees():
    user = db.session.get(User, session['user_id'])
    if user.is_admin:
        submissions = Submission.query.order_by(Submission.submitted_at.desc()).all()
        enrollments = Enrollment.query.order_by(Enrollment.enrolled_at.desc()).all()
    else:
        my_assessments = Assessment.query.filter_by(trainer_id=user.id).all()
        asm_ids = [a.id for a in my_assessments]
        submissions = Submission.query.filter(Submission.assessment_id.in_(asm_ids)).order_by(Submission.submitted_at.desc()).all()

        my_courses = Course.query.filter_by(trainer_id=user.id).all()
        c_ids = [c.id for c in my_courses]
        enrollments = Enrollment.query.filter(Enrollment.course_id.in_(c_ids)).order_by(Enrollment.enrolled_at.desc()).all()

    return render_template('trainer/trainees.html', submissions=submissions, enrollments=enrollments)

@trainer_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@role_required(['trainer', 'admin'])
def upload_materials():
    user = db.session.get(User, session['user_id'])
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        resource_type = request.form.get('resource_type', 'video').strip()
        category = request.form.get('category', 'Technology').strip()
        course_id = request.form.get('course_id', type=int)
        external_url = request.form.get('external_url', '').strip()
        duration = request.form.get('duration', '45 mins').strip()
        file = request.files.get('resource_file')

        if not title:
            flash('Please enter a title for the video lecture or resource.', 'error')
            return redirect(url_for('trainer.upload_materials'))

        file_or_url = external_url
        file_size = 'Stream / Web Video' if resource_type == 'video' else 'Web Link'

        if file and file.filename:
            fname = secure_filename(f"res_{uuid.uuid4().hex[:8]}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], fname)
            file.save(filepath)
            file_or_url = f"/static/uploads/{fname}"
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            file_size = f"{size_mb:.1f} MB"

        if not file_or_url:
            flash('Please select a video/document file to upload or enter a video streaming URL.', 'error')
            return redirect(url_for('trainer.upload_materials'))

        new_resource = Resource(
            title=title,
            description=description,
            resource_type=resource_type,
            file_or_url=file_or_url,
            category=category,
            course_id=course_id if course_id else None,
            trainer_id=user.id,
            file_size=file_size,
            duration=duration
        )
        db.session.add(new_resource)
        db.session.commit()
        flash(f'Successfully uploaded "{title}" to the Trainer Library!', 'success')
        return redirect(url_for('trainer.upload_materials'))

    # GET request: load courses and user's uploaded resources
    courses = Course.query.all()
    if user.is_admin:
        my_resources = Resource.query.order_by(Resource.created_at.desc()).all()
    else:
        my_resources = Resource.query.filter_by(trainer_id=user.id).order_by(Resource.created_at.desc()).all()

    return render_template('trainer/upload.html', courses=courses, resources=my_resources)

@trainer_bp.route('/delete-resource/<int:resource_id>', methods=['POST'])
@login_required
@role_required(['trainer', 'admin'])
def delete_resource(resource_id):
    user = db.session.get(User, session['user_id'])
    res = db.session.get(Resource, resource_id)
    if not res:
        abort(404)
    if not user.is_admin and res.trainer_id != user.id:
        flash('You do not have permission to delete this resource.', 'error')
        return redirect(url_for('trainer.upload_materials'))

    db.session.delete(res)
    db.session.commit()
    flash(f'Resource "{res.title}" was removed.', 'info')
    return redirect(url_for('trainer.upload_materials'))
