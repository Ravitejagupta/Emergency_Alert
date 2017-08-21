# app/home/views.py
import pyodbc
import json
import collections
import requests
import ast
import json
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

from firebase import firebase
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import home
from . forms import IssueForm, QueryForm, SubIssueForm
from .. import db
from ..models import Employee, Issue, SubIssue, Query

firebaseget = firebase.FirebaseApplication('https://eager-621db.firebaseio.com/Reports/')
firebasepost = firebase.FirebaseApplication('https://eager-621db.firebaseio.com/VerifiedReports/')

d = {}

@home.route('/')
def homepage():
	print("home page")
	return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():

	queries = Query.query.filter_by(is_admin = True)
	form = QueryForm()
	return render_template('home/dashboard.html', queries = queries, title="Dashboard")


@home.route('/reportissue',methods=['GET', 'POST'])
@login_required
def list_user_issues():
	issues = Issue.query.all()
	subissues = SubIssue.query.all()
	form = IssueForm()
	form.name.choices = [(issue.id,issue.name) for issue in issues]

	if (form.name.data != "None"):
		issue_id = form.name.data

		return redirect(url_for('home.select_sub_issue', id=issue_id))

	return render_template('home/reportissue.html',issues = issues,subissues = subissues,form = form, title = "Report an Issue")


@home.route('/reportissue/selectsubissue/<string:id>',methods=['GET', 'POST'])
@login_required
def select_sub_issue(id):
	subissues = SubIssue.query.filter_by(issue_id = id)
	form = SubIssueForm()
	form.subissue.query = subissues
	form.subissue.choices = [(subissue.id,subissue.name) for subissue in subissues]
	if (form.subissue.data != "None"):
		subissue = request.form['subissue']
		subissue_id = form.subissue.data
		print(subissue_id,subissue)
		additional_info = form.additional_info.data
		send_url = 'http://freegeoip.net/json'
		r = requests.get(send_url)
		j = json.loads(r.text)
		lat = j['latitude']
		lon = j['longitude']
		location = str(lat) + "," + str(lon)
		phone = form.phone.data
		if(carrier._is_mobile(number_type(phonenumbers.parse(phone)))) and phone !='':
			query = Query(employee_id=current_user.id, issue_id =id, subissue_id = subissue_id, additional_info = additional_info, location = location, phone = phone, zip_code = j['zip_code'])
			try:
				db.session.add(query)
				db.session.commit()
				flash('You have successfully added a query')
			except:
				flash('Error: Query already exists.')
		else:
			flash('Please enter a valid contact number')
			return redirect(url_for('home.select_sub_issue', id=id))


		return redirect(url_for('home.list_user_issues'))

	return render_template('home/selectsubissue.html',subissues = subissues,form = form, title = "Select Sub Issue")


@home.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
	dataset = []
	allData = []
	header = ['User', 'Issue', 'SubIssue', 'additional_info', 'Phone', 'latitude', 'longitude', 'zip_code']
	row = []
	queries = Query.query.all()
	for q in queries:
		row.append(q.location.split(',')[0])
		row.append(q.location.split(',')[1])
		row.append(q.zip_code)
		dataset.append([float(x) for x in row])
		row = []

	for q in queries:
		row.append(q.employee.username)
		row.append(q.issue.name)
		row.append(q.subissue.name)
		row.append(q.additional_info)
		row.append(q.phone)
		row.append(q.location.split(',')[0])
		row.append(q.location.split(',')[1])
		row.append(q.zip_code)
		allData.append([x for x in row])
		row = []

	o_dataset = np.array(dataset)

	##numpy columns
	X = o_dataset[:,0]
	Y = o_dataset[:,1]
	Z = o_dataset[:,2]
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	nb_clusters = 3
	colors = ["g","r","b"]
	kmeans = KMeans(n_clusters=nb_clusters)
	kmeans.fit(o_dataset)

	centriods = kmeans.cluster_centers_
	labels = kmeans.labels_

	clusters = []
	clusters_issues = []
	for c in range(nb_clusters):
		##only for plotting
		clusters.append([])
		##for json
		clusters_issues.append([])

	for c in range(nb_clusters):
		for i in range(len(o_dataset)):
			if labels[i]==c:
				clusters[c].append(o_dataset[i])
				clusters_issues[c].append(allData[i])

	resultDict = {}
	counter = 0
	for cluster in clusters_issues:
		df = pd.DataFrame(cluster, columns=header,index=['row_{0}'.format(x) for x in range(len(cluster))])
		df = df.transpose()
		jsonObject = df.to_dict()
		resultDict["cluster{0}".format(counter)] = jsonObject
		counter+=1

	out_json = json.dumps(resultDict)
	get = firebaseget.get('/ClusteredData',None)

	if(get is None):
		post = firebasepost.post('/ClusteredData',ast.literal_eval(out_json))

	count=0
	for i in ast.literal_eval(out_json):
		if ast.literal_eval(out_json)[i] != {}:
			count+=1
	cluster_size = len(ast.literal_eval(out_json)['cluster0'])

	json_dict = ast.literal_eval(out_json)

	for i in range(c):
		json_dict['cluster{}'.format(i)]['User'] = ""
		json_dict['cluster{}'.format(i)]['Issue'] = ""
		json_dict['cluster{}'.format(i)]['SubIssue'] = ""
		json_dict['cluster{}'.format(i)]['additional_info'] = ""
		for j in range(3):
			json_dict['cluster{}'.format(i)]['User'] +=  json_dict['cluster{}'.format(i)]['row_{}'.format(j)]['User'] + ', '
			json_dict['cluster{}'.format(i)]['Issue'] +=  json_dict['cluster{}'.format(i)]['row_{}'.format(j)]['Issue'] + ', '
			json_dict['cluster{}'.format(i)]['SubIssue'] +=  json_dict['cluster{}'.format(i)]['row_{}'.format(j)]['SubIssue'] + ', '
			json_dict['cluster{}'.format(i)]['additional_info'] +=  json_dict['cluster{}'.format(i)]['row_{}'.format(j)]['additional_info'] + ', '

	final_json = {}
	for i in range(c):
		row_dict = {}
		row_dict['User'] = json_dict['cluster{}'.format(i)]['User']
		row_dict['Issue'] = json_dict['cluster{}'.format(i)]['Issue']
		row_dict['SubIssue'] = json_dict['cluster{}'.format(i)]['SubIssue']
		row_dict['additional_info'] = json_dict['cluster{}'.format(i)]['additional_info']
		row_dict['location'] = json_dict['cluster{}'.format(i)]['row_0']['latitude'] + ',' + json_dict['cluster{}'.format(i)]['row_0']['longitude']
		row_dict['phone'] = json_dict['cluster{}'.format(i)]['row_0']['Phone']
		row_dict['zip_code'] = json_dict['cluster{}'.format(i)]['row_0']['zip_code']
		final_json['cluster{}'.format(i)] = row_dict

	counter = 0
	for cluster in clusters:
		data = np.array(cluster)
		if cluster != []:
			X = data[:,0]
			Y = data[:,1]
			Z = data[:,2]
		ax.scatter(X, Y, Z, c=colors[counter], marker='o')
		counter+=1

	ax.scatter(centriods[:,0],centriods[:,1],centriods[:,2], c = 'black', marker='x')


	form = QueryForm()

	return render_template('home/admin_dashboard.html',form = form, queries = queries, title="Admin Dashboard",content = list(final_json.values()))


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
	verified_query.is_admin = True
	db.session.commit()
	post = firebasepost.post('/VerifiedReports',{verified_query.issue.name:{0:verified_query.subissue.name, 1:"Additional Info: " + verified_query.additional_info},'phone':verified_query.phone,'latitude':verified_query.location.split(',')[0],'longitude':verified_query.location.split(',')[1]})

	return redirect(url_for('home.admin_dashboard'))

@home.route('/subscribe',methods=['GET', 'POST'])
@login_required
def subscribe():
	"""
	subscribe
	"""
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	flash('Subscribed successfully')
	post = firebasepost.post('/notificationRequests',{'user':current_user.username,'zip code':j['zip_code']})
	return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/test', methods=['GET', 'POST'])
def index():
	content = {1:22,4:1}
	return render_template('home/test.html',content = content)
