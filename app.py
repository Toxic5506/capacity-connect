import os
from datetime import datetime, timezone
from flask import Flask, render_template, session, abort
from config import Config
from models import db, User, Course, Enrollment, Announcement, Certificate
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.courses import courses_bp
from routes.assessments import assessments_bp
from routes.trainer import trainer_bp
from routes.library import library_bp
from routes.admin import admin_bp
from routes.competency import competency_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(assessments_bp)
    app.register_blueprint(trainer_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(competency_bp)

    @app.context_processor
    def inject_global_vars():
        user = None
        user_id = session.get('user_id')
        pending_count = 0
        if user_id:
            user = db.session.get(User, user_id)
            if user and user.is_admin:
                pending_count = User.query.filter_by(status='pending').count()
        return {
            'current_user': user,
            'pending_users_count': pending_count,
            'now': datetime.now(timezone.utc)
        }

    @app.route('/')
    @app.route('/landing')
    def landing():
        user = None
        user_id = session.get('user_id')
        if user_id:
            user = db.session.get(User, user_id)

        courses_count = Course.query.count()
        featured_courses = Course.query.order_by(Course.is_featured.desc(), Course.created_at.desc()).limit(6).all()
        announcements = Announcement.query.order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc()).all()
        trainers = User.query.filter_by(role='trainer', status='approved').all()

        return render_template('landing.html',
                               current_user=user,
                               courses_count=courses_count,
                               featured_courses=featured_courses,
                               announcements=announcements,
                               trainers=trainers)

    @app.route('/dashboard')
    def dashboard():
        user = None
        user_id = session.get('user_id')
        if user_id:
            user = db.session.get(User, user_id)
        else:
            # Default to Mayank (Admin) for immediate demonstration matching Screenshot 1
            user = User.query.filter_by(email='mayank@capacityconnect.org').first()
            if user:
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_role'] = user.role

        courses_count = Course.query.count()
        enrollments_count = Enrollment.query.filter_by(user_id=user.id).count() if user else 0
        announcements_count = Announcement.query.count()
        cert_count = Certificate.query.filter_by(user_id=user.id).count() if user else 0

        announcements = Announcement.query.order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc()).all()
        featured_courses = Course.query.order_by(Course.is_featured.desc(), Course.created_at.desc()).limit(6).all()

        return render_template('home.html',
                               user=user,
                               courses_count=courses_count,
                               enrollments_count=enrollments_count,
                               announcements_count=announcements_count,
                               cert_count=cert_count,
                               announcements=announcements,
                               featured_courses=featured_courses)

    @app.route('/home')
    def home():
        return dashboard()

    @app.route('/certificate/<cert_code>')
    def view_certificate(cert_code):
        cert = Certificate.query.filter_by(cert_code=cert_code).first()
        if not cert:
            abort(404)
        return render_template('certificate.html', cert=cert)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
