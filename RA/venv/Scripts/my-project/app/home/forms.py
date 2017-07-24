from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Issue, SubIssue


class IssueForm(FlaskForm):
    """
    Form for admin to add or edit an issue
    """
    name = QuerySelectField(query_factory=lambda: Issue.query.all(),
                                  get_label="name")
    # description = StringField('Description', validators=[DataRequired()])
    subissue = QuerySelectField(query_factory=lambda: SubIssue.query.all(),
                                  get_label="name")

    submit = SubmitField('Submit')


class QueryForm(FlaskForm):
    """
    List all Queries.
    """
    query_name = QuerySelectField(query_factory=lambda: Query.query.all(),
                                  get_label="name")
