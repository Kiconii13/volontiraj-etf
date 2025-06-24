from flask import request, jsonify, Blueprint, render_template, url_for, flash
from flask_login import login_required, current_user
from models import db, Project
from permissions import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin")
@login_required
@role_required('admin')
def admin():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('admin_console.html', projects=projects)

@admin_bp.route("/approve_project/<int:project_id>", methods=["POST"])
@login_required
@role_required('admin')
def approve_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.approved = True
    project.ongoing = True
    db.session.commit()
    return jsonify(success=True)

@admin_bp.route("/delete_project/<int:project_id>", methods=["POST"])
@login_required
@role_required('admin')
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify(success=True)

@admin_bp.route("/suspend_project/<int:project_id>", methods=["POST"])
@login_required
@role_required('admin')
def suspend_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.approved = False
    db.session.commit()
    return jsonify(success=True)
