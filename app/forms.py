from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields import (
    BooleanField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length

from app.controllers.region_controller import RegionController


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(1, 64)],
        render_kw={"autofocus": True},
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in", default=True)
    submit = SubmitField("Log In")


class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(1, 64)],
        render_kw={"autofocus": True},
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class CreateCellarForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(1, 64)],
        render_kw={"autofocus": True},
    )
    submit = SubmitField("Create it")


class RenameCellarForm(FlaskForm):
    new_name = StringField(
        "Name",
        validators=[DataRequired(), Length(1, 64)],
    )
    submit = SubmitField("Rename")


class CreateShelfForm(FlaskForm):
    number = IntegerField(
        "Number",
        validators=[DataRequired()],
    )
    region = SelectField(
        "Region",
        coerce=str,
    )
    bottles_per_shelf = IntegerField(
        "Number of bottles",
        validators=[DataRequired()],
    )
    submit = SubmitField("Create")

    def __init__(self, *args, **kwargs):
        super(CreateShelfForm, self).__init__(*args, **kwargs)
        # Dynamically set choices for the region field after app context is available
        self.region.choices = [
            (region.id, region.name) for region in RegionController.get_all()
        ]


class DeleteCellarForm(FlaskForm):
    submit = SubmitField("Delete cellar")
