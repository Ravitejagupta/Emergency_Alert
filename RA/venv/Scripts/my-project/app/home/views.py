# app/home/views.py
import pyodbc
import json
import collections

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import home
from . forms import IssueForm, QueryForm, SubIssueForm
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
	form.name.choices = [(issue.id,issue.name) for issue in issues]
	print("before")
	print(form.name.data)
	# if (form.validate_on_submit()):
	if (form.name.data is None):
		print("Hello")
		issue_id = form.name.data
		print(form.name.data)
		# print(int(issue_id))
		# issue_id = int(form.name.data)
		# print(form.name.data)
		return redirect(url_for('home.select_sub_issue', id=issue_id))

		# subissue = request.form['subissue']
		# additional_info = form.additional_info.data
		# location = form.location.data
		# query = Query(employee_id=current_user.id, issue_id =issue, subissue_id = subissue, additional_info = additional_info, location = location)
		# try:
		# 	db.session.add(query)
		# 	db.session.commit()
		# 	flash('You have successfully added a query')
		# except:
		# 	flash('Error: Query already exists.')
		# return redirect(url_for('home.select_sub_issue', id=20))

	return render_template('home/reportissue.html',issues = issues,subissues = subissues,form = form, title = "Report an Issue")


@home.route('/reportissue/selectsubissue/<string:id>',methods=['GET', 'POST'])
@login_required
def select_sub_issue(id):
	subissues = SubIssue.query.filter_by(issue_id = id)
	form = SubIssueForm()
	print(id)
	form.subissue.query = subissues
	return render_template('home/selectsubissue.html',subissues = subissues,form = form, title = "Select Sub Issue")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
# prevent non-admins from accessing the page
# if not current_user.is_admin:
#     abort(403)

	queries = Query.query.all()
	form = QueryForm()
	return render_template('home/admin_dashboard.html',form = form, queries = queries, title="Admin Dashboard")


#delete a query
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
	print(id)
	print(verified_query)
	verified_query_details = []
	# for k in verified_query:
	# 	verified_query_details.append(k)
	# verified_query_tuple = (str(verified_query.employee.username), str(verified_query.issue.name), str(verified_query.subissue.name) )
	# verified_query_details.append(verified_query_tuple)

	j = json.dumps(verified_query_details)
	verified_query_details_file = 'verified_query_details_file.js'
	text_file = 'text_file.txt'
	f = open(text_file,'w')
	print(f,str(verified_query.employee.username))


	return redirect(url_for('home.admin_dashboard'))
