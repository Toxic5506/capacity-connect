from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models import db, User, Course, Enrollment, Assessment, Submission, Certificate, Resource, Announcement, Competency
from routes.auth import login_required, role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users')
@login_required
@role_required(['admin'])
def users():
    role_filter = request.args.get('role', '').strip()
    status_filter = request.args.get('status', '').strip()
    search = request.args.get('search', '').strip()

    query = User.query
    if role_filter and role_filter != 'all':
        query = query.filter_by(role=role_filter)
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if search:
        query = query.filter((User.name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))

    all_users = query.order_by(User.created_at.desc()).all()
    pending_count = User.query.filter_by(status='pending').count()

    return render_template('admin/users.html',
                           users=all_users,
                           pending_count=pending_count,
                           selected_role=role_filter,
                           selected_status=status_filter,
                           search=search)

@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@login_required
@role_required(['admin'])
def approve_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    action = request.form.get('action', 'approve')
    if action == 'approve':
        user.status = 'approved'
        flash(f'User {user.name} has been approved.', 'success')
    elif action == 'reject':
        user.status = 'rejected'
        flash(f'User {user.name} has been rejected.', 'warning')
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@login_required
@role_required(['admin'])
def change_role(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    new_role = request.form.get('role')
    if new_role in ['trainee', 'trainer', 'admin']:
        user.role = new_role
        db.session.commit()
        flash(f'Role for {user.name} changed to {new_role.title()}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/dashboard')
@login_required
@role_required(['admin'])
def dashboard():
    total_trainees = User.query.filter_by(role='trainee').count()
    total_trainers = User.query.filter_by(role='trainer').count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    total_certifications = Certificate.query.count()
    total_assessments = Assessment.query.count()
    total_resources = Resource.query.count()

    all_subs = Submission.query.all()
    avg_score = round(sum(s.score for s in all_subs) / len(all_subs), 1) if all_subs else 84.5
    pass_count = sum(1 for s in all_subs if s.passed)
    pass_rate = round((pass_count / len(all_subs)) * 100, 1) if all_subs else 88.0

    courses = Course.query.all()
    cat_counts = {}
    for c in courses:
        cat_counts[c.category] = cat_counts.get(c.category, 0) + 1

    recent_enrollments = Enrollment.query.order_by(Enrollment.enrolled_at.desc()).limit(6).all()
    recent_submissions = Submission.query.order_by(Submission.submitted_at.desc()).limit(6).all()

    return render_template('admin/dashboard.html',
                           total_trainees=total_trainees,
                           total_trainers=total_trainers,
                           total_courses=total_courses,
                           total_enrollments=total_enrollments,
                           total_certifications=total_certifications,
                           total_assessments=total_assessments,
                           total_resources=total_resources,
                           avg_score=avg_score,
                           pass_rate=pass_rate,
                           cat_counts=cat_counts,
                           recent_enrollments=recent_enrollments,
                           recent_submissions=recent_submissions)

@admin_bp.route('/announcements', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def announcements():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            tag = request.form.get('tag', 'Announcement')
            is_pinned = bool(request.form.get('is_pinned'))

            if title and content:
                ann = Announcement(
                    title=title,
                    content=content,
                    tag=tag,
                    author_name=session.get('user_name', 'Admin Team'),
                    author_id=session.get('user_id'),
                    is_pinned=is_pinned
                )
                db.session.add(ann)
                db.session.commit()
                flash('Announcement published to homepage feed!', 'success')

        elif action == 'delete':
            ann_id = int(request.form.get('ann_id'))
            ann = db.session.get(Announcement, ann_id)
            if ann:
                db.session.delete(ann)
                db.session.commit()
                flash('Announcement removed.', 'info')

        return redirect(url_for('admin.announcements'))

    all_announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=all_announcements)

@admin_bp.route('/competency-matrix', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def competency_matrix():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_competency':
            name = request.form.get('name', '').strip()
            category = request.form.get('category', 'Technology').strip()
            trainer_id = request.form.get('trainer_id', type=int)
            proficiency = request.form.get('proficiency_level', 'Expert')
            years = int(request.form.get('years_experience', 3))

            if name and trainer_id:
                comp = Competency(
                    name=name,
                    category=category,
                    trainer_id=trainer_id,
                    proficiency_level=proficiency,
                    years_experience=years
                )
                db.session.add(comp)
                db.session.commit()
                flash(f'Mapped competency "{name}" to trainer.', 'success')

        elif action == 'assign_course_trainer':
            course_id = int(request.form.get('course_id'))
            trainer_id = int(request.form.get('trainer_id'))
            c = db.session.get(Course, course_id)
            if c:
                c.trainer_id = trainer_id
                db.session.commit()
                flash(f'Assigned trainer to course: {c.title}.', 'success')

        return redirect(url_for('admin.competency_matrix'))

    competencies = Competency.query.all()
    trainers = User.query.filter(User.role.in_(['trainer', 'admin'])).all()
    courses = Course.query.all()

    return render_template('admin/competency.html',
                           competencies=competencies,
                           trainers=trainers,
                           courses=courses)
