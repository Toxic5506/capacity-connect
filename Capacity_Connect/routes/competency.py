from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Course, Competency
from routes.auth import login_required

competency_bp = Blueprint('competency', __name__)

@competency_bp.route('/competency-mapping', methods=['GET', 'POST'])
@login_required
def matrix():
    user = db.session.get(User, session['user_id'])
    
    # Handle Competency actions
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_competency':
            name = request.form.get('name', '').strip()
            category = request.form.get('category', 'Technology').strip()
            # If trainer, self-assign; if admin, use selected trainer
            if user.is_admin:
                trainer_id = request.form.get('trainer_id', type=int)
            else:
                trainer_id = user.id
                
            proficiency = request.form.get('proficiency_level', 'Expert')
            years = int(request.form.get('years_experience', 3))

            if name and trainer_id:
                comp = Competency(
                    name=name,
                    category=category,
                    trainer_id=trainer_id,
                    proficiency_level=proficiency,
                    years_experience=years,
                    is_verified=True
                )
                db.session.add(comp)
                db.session.commit()
                flash(f'Successfully mapped competency "{name}" to trainer.', 'success')

        elif action == 'assign_course_trainer' and user.is_admin:
            course_id = int(request.form.get('course_id'))
            trainer_id = int(request.form.get('trainer_id'))
            c = db.session.get(Course, course_id)
            if c:
                c.trainer_id = trainer_id
                db.session.commit()
                flash(f'Successfully assigned trainer to course: "{c.title}".', 'success')

        return redirect(url_for('competency.matrix'))

    # Load data
    competencies = Competency.query.all()
    trainers = User.query.filter(User.role.in_(['trainer', 'admin'])).all()
    courses = Course.query.all()

    # Pre-calculate distinct subject areas for the Identification Engine
    subjects = list(set([c.name for c in competencies] + [crs.category for crs in courses]))
    subjects.sort()

    return render_template('competency/index.html',
                           competencies=competencies,
                           trainers=trainers,
                           courses=courses,
                           subjects=subjects)
