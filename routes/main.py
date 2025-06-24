from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from models import db, User, Project, Volunteers

main_bp = Blueprint('main', __name__)

@login_required
@main_bp.route('/main', methods=['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        return render_template('main.html')
    else:
        return redirect(url_for('auth.index'))

@login_required
@main_bp.route('/make_project', methods=['GET', 'POST'])
def make_project():
    if request.method == 'POST':
        project = Project()
        project.name = request.form['name']
        project.description = request.form['description']
        project.number_required = request.form['number']
        project.owner_id = current_user.id
        db.session.add(project)
        db.session.commit()
        flash('Tvoj projekat je kreiran i poslat administratoru na pregled!')
        return redirect(url_for('main.main'))
    return render_template('make_project.html')

@login_required
@main_bp.route('/projects', methods=['GET', 'POST'])
def projects():
    projects = Project.query.order_by(Project.id.desc()).filter(Project.approved == True).all()
    return render_template('projects.html', projects=projects)

@main_bp.route('/projekti-fragment')
def projekti_fragment():
    projects = Project.query.order_by(Project.id.desc()).filter(Project.approved == True).all()
    return render_template('projects_fragment.html', projects=projects)

@login_required
@main_bp.route('/my_projects')
def my_projects():
    projects = Project.query.order_by(Project.id.desc()).filter(Project.owner_id == current_user.id and Project.approved == True).all()
    return render_template('my_projects.html', projects=projects)

@main_bp.route('/apply/<int:project_id>', methods=['POST'])
@login_required
def apply_to_project(project_id):
    project = Project.query.get_or_404(project_id)

    # Provera da li je korisnik već prijavljen
    already_applied = Volunteers.query.filter_by(user_id=current_user.id, project_id=project.id).first()
    if already_applied:
        return jsonify({'message': 'Već si prijavljen na ovaj projekat.'})

    # Kreiraj vezu
    new_volunteer = Volunteers(user_id=current_user.id, project_id=project.id)
    db.session.add(new_volunteer)
    db.session.commit()

    return jsonify({'message': 'Uspešno si se prijavio na projekat!'})

@main_bp.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    # Zabrani ako nije došao sa tvoje stranice
    referer = request.headers.get("Referer", "")
    allowed_sources = [request.host_url + "my_projects", request.host_url + "projects",
                       request.host_url + "admin_console"]

    if not any(referer.startswith(src) for src in allowed_sources) and current_user.role != 'admin':
        abort(403)  # Forbidden

    user = User.query.get_or_404(user_id)
    return render_template("view-volunteer.html", user=user)

