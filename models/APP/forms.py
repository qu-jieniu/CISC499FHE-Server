from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms_validators import AlphaNumeric
import re

class IPForm(FlaskForm):
    ip = StringField('Server IP', validators=[IPAddress(), DataRequired()], render_kw={"placeholder": '192.168.1.1'})
    port = IntegerField('Port', validators=[DataRequired()], render_kw={"placeholder": '80'})
    submit = SubmitField('Connect')

class configNewSession(FlaskForm):
    class Meta:
        def render_field(self, field, render_kw):
            if field.type == "_Option":
                render_kw.setdefault("required", True)
            return super().render_field(field, render_kw)
    session_name = StringField('Session Name', validators=[DataRequired(), AlphaNumeric()])
    key_size = RadioField('Key Size', validators=[DataRequired()], choices=[('512','512 Bits'),('1024','1024 Bits'), ('2048','2048 Bits'), ('4096','4096 Bits')])
    data_type = RadioField('Data Type', validators=[DataRequired()], choices=[('Integer', "Integer"), ('Polynomial', "Polynomial")])
    submit = SubmitField('Create')

class configOldSession(FlaskForm):
    file = FileField()
    upload = SubmitField('Upload')

class dataEntry_int(FlaskForm):
    data_label_int = StringField("Label", validators=[DataRequired(), AlphaNumeric()], render_kw={'placeholder':'numOfPhone'})
    data_field_int = IntegerField('Data', validators=[DataRequired()], render_kw={"placeholder": '10'})
    submit_int = SubmitField("Submit")


class dataEntry_poly(FlaskForm):
    def validate_poly(form, field):
        if not re.match(r"^([+-]?(?:(?:\d+x\^\d+)|(?:\d+x)|(?:\d+)|(?:x)))+$", field.data):
            raise ValidationError('Incorrect form of polynomial (Single-variable)')

    data_label_poly = StringField("Label", validators=[DataRequired(), AlphaNumeric()], render_kw={'placeholder':'numOfPhone'})
    data_field_poly = StringField('Data',validators=[DataRequired(), validate_poly], render_kw={"placeholder":"2x + 10"})
    submit_poly = SubmitField("Submit")
