import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from models import db, Course, Resource
from routes.auth import login_required, role_required

library_bp = Blueprint('library', __name__, url_prefix='/library')

@library_bp.route('')
def index():
    rtype = request.args.get('type', '').strip()
    search = request.args.get('search', '').strip()

    query = Resource.query
    if rtype and rtype != 'all':
        query = query.filter_by(resource_type=rtype)
    if search:
        query = query.filter((Resource.title.ilike(f"%{search}%")) | (Resource.description.ilike(f"%{search}%")))

    resources = query.order_by(Resource.created_at.desc()).all()
    courses = Course.query.all()

    return render_template('library/index.html',
                           resources=resources,
                           courses=courses,
                           selected_type=rtype,
                           search=search)

@library_bp.route('/upload', methods=['POST'])
@login_required
@role_required(['trainer', 'admin'])
def upload_resource():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    resource_type = request.form.get('resource_type', 'document')
    category = request.form.get('category', 'General').strip()
    course_id = request.form.get('course_id', type=int)
    external_url = request.form.get('external_url', '').strip()
    file = request.files.get('resource_file')

    if not title:
        flash('Resource title is required.', 'error')
        return redirect(url_for('library.index'))

    file_or_url = external_url
    file_size = 'Web Link'
    duration = request.form.get('duration', '30 mins')

    if file and file.filename:
        fname = secure_filename(f"res_{uuid.uuid4().hex[:8]}_{file.filename}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], fname)
        file.save(filepath)
        file_or_url = f"/static/uploads/{fname}"
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        file_size = f"{size_mb:.1f} MB"

    if not file_or_url:
        flash('Please upload a file or specify a video/document URL.', 'error')
        return redirect(url_for('library.index'))

    res = Resource(
        title=title,
        description=description,
        resource_type=resource_type,
        file_or_url=file_or_url,
        category=category,
        course_id=course_id if course_id else None,
        trainer_id=session['user_id'],
        file_size=file_size,
        duration=duration
    )
    db.session.add(res)
    db.session.commit()
    flash(f'Resource "{title}" has been published to the Trainer Library!', 'success')
    return redirect(url_for('library.index'))
