from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Profile

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'info')
                return redirect(url_for('auth.login'))
            user = db.session.get(User, session['user_id'])
            if not user or user.role not in roles:
                flash('You do not have permission to access that area.', 'error')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if user.status == 'pending':
                flash('Your registration is currently pending Administrator approval. Please check back soon.', 'warning')
                return render_template('auth/login.html')
            if user.status == 'rejected':
                flash('Your account access has been restricted. Please contact support.', 'error')
                return render_template('auth/login.html')

            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid email address or password.', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/quick-login/<role>')
def quick_login(role):
    user = None
    if role == 'admin':
        user = User.query.filter_by(email='mayank@capacityconnect.org').first()
    elif role == 'trainer':
        user = User.query.filter_by(email='trainer.sarah@capacityconnect.org').first()
    elif role == 'trainee':
        user = User.query.filter_by(email='trainee.alex@capacityconnect.org').first()

    if user:
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_role'] = user.role
        flash(f'Signed in as {user.name} ({user.role.title()})', 'success')
    return redirect(url_for('home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'trainee').lower()
        job_title = request.form.get('job_title', 'Professional').strip()
        organization = request.form.get('organization', '').strip()

        if not name or not email or not password:
            flash('Please fill in all required fields.', 'error')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with this email address already exists.', 'error')
            return render_template('auth/register.html')

        # All new account registrations require administrator approval
        status = 'pending'

        user = User(
            name=name,
            email=email,
            role=role,
            status=status,
            job_title=job_title
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = Profile(
            user_id=user.id,
            bio=f"{job_title} at {organization or 'Capacity Connect Network'}",
            organization=organization or "Capacity Connect Network"
        )
        db.session.add(profile)
        db.session.commit()

        flash('Registration submitted successfully! Your account is pending Administrator approval. Once an administrator approves your account, you will be able to sign in.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out successfully.', 'info')
    return redirect(url_for('auth.login'))
