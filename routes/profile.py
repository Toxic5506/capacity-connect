import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from models import db, User, Profile, Certificate, Enrollment
from routes.auth import login_required

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    user = db.session.get(User, session['user_id'])
    prof = user.profile
    if not prof:
        prof = Profile(user_id=user.id)
        db.session.add(prof)
        db.session.commit()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_basic':
            user.name = request.form.get('name', user.name).strip()
            user.job_title = request.form.get('job_title', user.job_title).strip()
            prof.bio = request.form.get('bio', prof.bio).strip()
            prof.organization = request.form.get('organization', prof.organization).strip()
            prof.department = request.form.get('department', prof.department).strip()
            prof.phone = request.form.get('phone', prof.phone).strip()
            prof.location = request.form.get('location', prof.location).strip()
            db.session.commit()
            flash('Profile information updated successfully.', 'success')

        elif action == 'add_qualification':
            degree = request.form.get('degree', '').strip()
            institution = request.form.get('institution', '').strip()
            year = request.form.get('year', '').strip()
            field = request.form.get('field', '').strip()
            if degree and institution:
                quals = prof.qualifications
                quals.append({'degree': degree, 'institution': institution, 'year': year, 'field': field})
                prof.qualifications = quals
                db.session.commit()
                flash('Qualification credential added.', 'success')

        elif action == 'delete_qualification':
            idx = int(request.form.get('index', -1))
            quals = prof.qualifications
            if 0 <= idx < len(quals):
                quals.pop(idx)
                prof.qualifications = quals
                db.session.commit()
                flash('Qualification removed.', 'info')

        elif action == 'add_experience':
            role_title = request.form.get('role', '').strip()
            company = request.form.get('company', '').strip()
            duration = request.form.get('duration', '').strip()
            desc = request.form.get('description', '').strip()
            if role_title and company:
                exp = prof.experience
                exp.append({'role': role_title, 'company': company, 'duration': duration, 'description': desc})
                prof.experience = exp
                db.session.commit()
                flash('Work experience record added.', 'success')

        elif action == 'delete_experience':
            idx = int(request.form.get('index', -1))
            exp = prof.experience
            if 0 <= idx < len(exp):
                exp.pop(idx)
                prof.experience = exp
                db.session.commit()
                flash('Experience entry removed.', 'info')

        elif action == 'update_skills':
            skills_str = request.form.get('skills', '')
            interests_str = request.form.get('interests', '')
            skills_list = [s.strip() for s in skills_str.split(',') if s.strip()]
            interests_list = [i.strip() for i in interests_str.split(',') if i.strip()]
            prof.skills = skills_list
            prof.interests = interests_list
            db.session.commit()
            flash('Skills & professional interests updated.', 'success')

        elif action == 'upload_certificate':
            cert_title = request.form.get('cert_title', '').strip()
            issuer = request.form.get('issuer', 'External Certification').strip()
            file = request.files.get('cert_file')
            if cert_title:
                file_path = ''
                if file and file.filename:
                    fname = secure_filename(f"cert_{uuid.uuid4().hex[:8]}_{file.filename}")
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fname))
                    file_path = f"/static/uploads/{fname}"

                new_cert = Certificate(
                    user_id=user.id,
                    cert_code=f"EXT-{uuid.uuid4().hex[:8].upper()}",
                    title=cert_title,
                    recipient_name=user.name,
                    issuer=issuer,
                    external_cert=True,
                    file_path=file_path
                )
                db.session.add(new_cert)
                db.session.commit()
                flash('Certificate uploaded successfully.', 'success')

        return redirect(url_for('profile.view_profile'))

    my_certificates = Certificate.query.filter_by(user_id=user.id).order_by(Certificate.issue_date.desc()).all()
    my_enrollments = Enrollment.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, profile=prof, certificates=my_certificates, enrollments=my_enrollments)
