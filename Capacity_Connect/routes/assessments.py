import json
import uuid
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models import db, User, Course, Assessment, Question, Submission, Certificate, Enrollment
from routes.auth import login_required

assessments_bp = Blueprint('assessments', __name__, url_prefix='/assessments')

@assessments_bp.route('')
def list_assessments():
    subject = request.args.get('subject', '').strip()
    query = Assessment.query.filter_by(is_active=True)
    if subject:
        query = query.filter_by(subject=subject)

    all_assessments = query.order_by(Assessment.created_at.desc()).all()
    subjects = db.session.query(Assessment.subject).distinct().all()
    subjects = [s[0] for s in subjects if s[0]]

    user_id = session.get('user_id')
    user_submissions = {}
    if user_id:
        subs = Submission.query.filter_by(user_id=user_id).all()
        for s in subs:
            if s.assessment_id not in user_submissions or s.score > user_submissions[s.assessment_id].score:
                user_submissions[s.assessment_id] = s

    return render_template('assessments/list.html',
                           assessments=all_assessments,
                           subjects=subjects,
                           selected_sub=subject,
                           user_submissions=user_submissions)

@assessments_bp.route('/<int:assessment_id>/take')
@login_required
def take_assessment(assessment_id):
    asm = db.session.get(Assessment, assessment_id)
    if not asm or not asm.is_active:
        flash('Assessment is currently inactive or not available.', 'error')
        return redirect(url_for('assessments.list_assessments'))

    questions = asm.questions.all()
    if not questions:
        flash('This assessment does not contain questions yet.', 'warning')
        return redirect(url_for('assessments.list_assessments'))

    return render_template('assessments/take.html', assessment=asm, questions=questions)

@assessments_bp.route('/<int:assessment_id>/submit', methods=['POST'])
@login_required
def submit_assessment(assessment_id):
    asm = db.session.get(Assessment, assessment_id)
    if not asm:
        abort(404)

    user = db.session.get(User, session['user_id'])
    questions = asm.questions.all()
    total_q = len(questions)

    if total_q == 0:
        flash('Assessment contains no questions.', 'error')
        return redirect(url_for('assessments.list_assessments'))

    correct_count = 0
    answers = {}

    for q in questions:
        user_ans = request.form.get(f'question_{q.id}', '').strip().upper()
        answers[str(q.id)] = user_ans
        if user_ans == q.correct_option.strip().upper():
            correct_count += 1

    score = round((correct_count / total_q) * 100, 1)
    passed = score >= asm.passing_score

    submission = Submission(
        user_id=user.id,
        assessment_id=asm.id,
        score=score,
        correct_count=correct_count,
        total_questions=total_q,
        passed=passed,
        answers_json=json.dumps(answers)
    )
    db.session.add(submission)
    db.session.flush()

    if passed:
        cert_code = f"CC-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"
        cert = Certificate(
            user_id=user.id,
            course_id=asm.course_id,
            assessment_id=asm.id,
            cert_code=cert_code,
            title=f"Competency Certification: {asm.subject}",
            recipient_name=user.name,
            score=score,
            issuer="Capacity Connect Digital Assessment Council"
        )
        db.session.add(cert)

        if asm.course_id:
            enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=asm.course_id).first()
            if enrollment:
                enrollment.progress = 100
                enrollment.status = 'completed'
                enrollment.completed_at = datetime.now(timezone.utc)

    db.session.commit()
    return redirect(url_for('assessments.assessment_result', submission_id=submission.id))

@assessments_bp.route('/result/<int:submission_id>')
@login_required
def assessment_result(submission_id):
    sub = db.session.get(Submission, submission_id)
    if not sub:
        abort(404)

    if sub.user_id != session['user_id'] and session.get('user_role') not in ['admin', 'trainer']:
        flash('Access restricted.', 'error')
        return redirect(url_for('assessments.list_assessments'))

    asm = sub.assessment
    questions = asm.questions.all()
    answers = sub.answers

    cert = Certificate.query.filter_by(user_id=sub.user_id, assessment_id=asm.id).order_by(Certificate.issue_date.desc()).first()

    return render_template('assessments/result.html',
                           submission=sub,
                           assessment=asm,
                           questions=questions,
                           answers=answers,
                           certificate=cert)
