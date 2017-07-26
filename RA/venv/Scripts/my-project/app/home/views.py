# app/home/views.py
import pyodbc
import json
import collections

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import home
from . forms import IssueForm, QueryForm
from .. import db
from ..models import Employee, Issue, SubIssue, Query

@home.route('/')
def homepage():
	print("home page")
	return render_template('home/index.html', title="Welcome")
	#return "hello wirld"

@home.route('/dashboard')
@login_required
def dashboard():
	return render_template('home/dashboard.html', title="Dashboard")


@home.route('/reportissue',methods=['GET', 'POST'])
@login_required
def list_user_issues():
	issues = Issue.query.all()
	subissues = SubIssue.query.all()
	form = IssueForm()
	if form.validate_on_submit():
		issue = request.form['name']
		# issue = Issue.query.filter(Issue.id == form.name.data.value).all()
		subissue = request.form['subissue']
		query = Query(employee_id=current_user.id, issue_id =issue, subissue_id = subissue)
		try:
			db.session.add(query)
			db.session.commit()
			flash('You have successfully added a query')
		except:
			flash('Error: Query already exists.')

	return render_template('home/reportissue.html',issues = issues,subissues = subissues,form = form, title = "Report an Issue")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
# prevent non-admins from accessing the page
# if not current_user.is_admin:
#     abort(403)

	queries = Query.query.all()
	form = QueryForm()
	return render_template('home/admin_dashboard.html',form = form, queries = queries, title="Admin Dashboard")


#delet a query
@home.route('/queries/delete/<int:id>', methods = ['GET','POST'])
@login_required
def delete_query(id):
	"""
    Delete a query from the database
    """
	# check_admin()

	deleted_query = Query.query.get_or_404(id)
	db.session.delete(deleted_query)
	db.session.commit()
	flash('You have successfully deleted the query.')

	return redirect(url_for('home.admin_dashboard'))


@home.route('/queries/verify/<int:id>', methods = ['GET','POST'])
@login_required
def verify_query(id):
	"""
	Verify a query
	"""
	# check_admin()
	verified_query = Query.query.get_or_404(id)
	verified_query_details = []
	# for k in verified_query:
	# 	verified_query_details.append(k)
	verified_query_tuple = (verified_query.employee.username, verified_query.issue.name, verified_query.subissue.name )
	verified_query_details.append(verified_query_tuple)

	j = json.dumps(verified_query_details)
	verified_query_details_file = 'verified_query_details_file.js'
	f = open(verified_query_details_file,'w')
	print(f,verified_query_details)


	return redirect(url_for('home.admin_dashboard'))
