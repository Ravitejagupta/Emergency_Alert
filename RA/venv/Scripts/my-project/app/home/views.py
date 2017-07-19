# app/home/views.py

from flask import abort, render_template
from flask_login import current_user, login_required

from . import home
from .. import db
from ..models import Employee, Issue, SubIssue

@home.route('/')
def homepage():
	print("home page")
	return render_template('home/index.html', title="Welcome")
	#return "hello wirld"

@home.route('/dashboard')
@login_required
def dashboard():
	return render_template('home/dashboard.html', title="Dashboard")


@home.route('/reportissue')
@login_required
def list_user_issues():
	issues = Issue.query.all()
	subissues = SubIssue.query.all()
	return render_template('home/reportissue.html',issues = issues,subissues = subissues, title = "Report an Issue")



@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
