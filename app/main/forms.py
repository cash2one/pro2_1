from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SelectField,SubmitField,BooleanField,RadioField
from wtforms.validators import Regexp,Required,EqualTo
from ..models import Staff
from wtforms import ValidationError


class StaffMessageForm(FlaskForm):
    staffid = StringField("员工编号")
    staffname = StringField("员工姓名")
    staffphone = StringField("联系方式")
    staffsex = RadioField("性别",choices=[('A','男'),('B','女')])
    submit = SubmitField("查询")
