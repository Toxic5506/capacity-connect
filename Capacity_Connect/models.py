import json
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utcnow():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='trainee', nullable=False)  # 'trainee', 'trainer', 'admin'
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'approved', 'pending', 'rejected'
    job_title = db.Column(db.String(120), default='Professional')
    avatar = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=utcnow)

    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete-orphan")
    enrollments = db.relationship('Enrollment', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    submissions = db.relationship('Submission', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    certificates = db.relationship('Certificate', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    resources = db.relationship('Resource', backref='trainer', lazy='dynamic')
    taught_courses = db.relationship('Course', backref='trainer', lazy='dynamic')
    feedbacks = db.relationship('Feedback', backref='user', lazy='dynamic')
    competencies = db.relationship('Competency', backref='trainer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def initials(self):
        parts = self.name.strip().split()
        if not parts:
            return "U"
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_trainer(self):
        return self.role == 'trainer'

    @property
    def is_trainee(self):
        return self.role == 'trainee'

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bio = db.Column(db.Text, default='')
    organization = db.Column(db.String(150), default='Capacity Connect Network')
    department = db.Column(db.String(120), default='General')
    phone = db.Column(db.String(50), default='')
    location = db.Column(db.String(120), default='')
    
    # Stored as JSON strings
    qualifications_json = db.Column(db.Text, default='[]')
    experience_json = db.Column(db.Text, default='[]')
    skills_json = db.Column(db.Text, default='[]')
    interests_json = db.Column(db.Text, default='[]')

    @property
    def qualifications(self):
        try:
            return json.loads(self.qualifications_json) if self.qualifications_json else []
        except Exception:
            return []

    @qualifications.setter
    def qualifications(self, val):
        self.qualifications_json = json.dumps(val)

    @property
    def experience(self):
        try:
            return json.loads(self.experience_json) if self.experience_json else []
        except Exception:
            return []

    @experience.setter
    def experience(self, val):
        self.experience_json = json.dumps(val)

    @property
    def skills(self):
        try:
            return json.loads(self.skills_json) if self.skills_json else []
        except Exception:
            return []

    @skills.setter
    def skills(self, val):
        self.skills_json = json.dumps(val)

    @property
    def interests(self):
        try:
            return json.loads(self.interests_json) if self.interests_json else []
        except Exception:
            return []

    @interests.setter
    def interests(self, val):
        self.interests_json = json.dumps(val)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='General')  # Management, Technology, Data Analytics, etc.
    level = db.Column(db.String(50), default='Beginner')     # Beginner, Intermediate, Advanced
    duration = db.Column(db.String(50), default='4 Weeks')
    thumbnail_url = db.Column(db.String(255), default='')
    syllabus = db.Column(db.Text, default='')
    is_featured = db.Column(db.Boolean, default=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic', cascade="all, delete-orphan")
    assessments = db.relationship('Assessment', backref='course', lazy='dynamic', cascade="all, delete-orphan")
    resources = db.relationship('Resource', backref='course', lazy='dynamic')
    feedbacks = db.relationship('Feedback', backref='course', lazy='dynamic', cascade="all, delete-orphan")

    @property
    def enrolled_count(self):
        return self.enrollments.count()

    @property
    def average_rating(self):
        all_fb = self.feedbacks.all()
        if not all_fb:
            return 5.0
        return round(sum(f.rating for f in all_fb) / len(all_fb), 1)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=utcnow)
    progress = db.Column(db.Integer, default=15)  # 0 to 100
    status = db.Column(db.String(50), default='in_progress')  # in_progress, completed
    completed_at = db.Column(db.DateTime, nullable=True)

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time_limit_minutes = db.Column(db.Integer, default=15)
    passing_score = db.Column(db.Integer, default=70)  # percentage
    deadline = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    # Relationships
    questions = db.relationship('Question', backref='assessment', lazy='dynamic', cascade="all, delete-orphan")
    submissions = db.relationship('Submission', backref='assessment', lazy='dynamic', cascade="all, delete-orphan")
    trainer = db.relationship('User', foreign_keys=[trainer_id], backref='created_assessments')

    @property
    def question_count(self):
        return self.questions.count()

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    explanation = db.Column(db.Text, default='')
    points = db.Column(db.Integer, default=1)

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)  # percentage
    correct_count = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    answers_json = db.Column(db.Text, default='{}')
    submitted_at = db.Column(db.DateTime, default=utcnow)

    @property
    def answers(self):
        try:
            return json.loads(self.answers_json) if self.answers_json else {}
        except Exception:
            return {}

class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=True)
    cert_code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    recipient_name = db.Column(db.String(150), nullable=False)
    issuer = db.Column(db.String(150), default='Capacity Connect Certification Board')
    score = db.Column(db.Float, nullable=True)
    issue_date = db.Column(db.DateTime, default=utcnow)
    external_cert = db.Column(db.Boolean, default=False)
    file_path = db.Column(db.String(255), default='')

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    resource_type = db.Column(db.String(50), default='presentation')  # video, presentation, document, link
    file_or_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), default='General')
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_size = db.Column(db.String(50), default='2.4 MB')
    duration = db.Column(db.String(50), default='45 mins')
    created_at = db.Column(db.DateTime, default=utcnow)

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(50), default='Announcement')  # Announcement, New Content, Notification, Achievement
    author_name = db.Column(db.String(100), default='Admin Team')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, default=5)
    comments = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=utcnow)

class Competency(db.Model):
    __tablename__ = 'competencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), default='Technology')
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    proficiency_level = db.Column(db.String(50), default='Expert')  # Expert, Advanced, Proficient
    years_experience = db.Column(db.Integer, default=5)
    is_verified = db.Column(db.Boolean, default=True)
