from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Issue, SubIssue
from wtforms import RadioField


class IssueForm(FlaskForm):
    """
    Form for user to add an issue
    """

    name = RadioField('name', choices=[])

    submit = SubmitField('Submit')


class QueryForm(FlaskForm):
    """
    List all Queries.
    """
    query_name = QuerySelectField(query_factory=lambda: Query.query.all(),
                                  get_label="name")

class SubIssueForm(FlaskForm):
    """
    List all sub issues in next page.
    """
    subissue = RadioField('Sub Issue', choices = [])

    additional_info = StringField('Additional info')

    # location = StringField('Location')

    phone = StringField('Phone')

    submit = SubmitField('Submit')
