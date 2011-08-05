from flaskext.wtf import *
from models import Project, Person, Bill

class ProjectForm(Form):
    name = TextField("Project name", validators=[Required()])
    id = TextField("Project identifier", validators=[Required()])
    password = PasswordField("Password", validators=[Required()])
    contact_email = TextField("Email", validators=[Required(), Email()])
    submit = SubmitField("Create the project")

    def save(self):
        """Create a new project with the information given by this form.

        Returns the created instance
        """
        project = Project(name=self.name.data, id=self.id.data, 
                password=self.password.data, 
                contact_email=self.contact_email.data)
        return project


class AuthenticationForm(Form):
    id = TextField("Project identifier", validators=[Required()])
    password = TextField("Password", validators=[Required()])
    submit = SubmitField("Get in")


class BillForm(Form):
    what = TextField("What?", validators=[Required()])
    payer = SelectField("Payer", validators=[Required()])
    amount = DecimalField("Amount payed", validators=[Required()])
    payed_for = SelectMultipleField("Who has to pay for this?", 
            validators=[Required()])
    submit = SubmitField("Add the bill")

    def save(self):
        bill = Bill(payer_id=self.payer.data, amount=self.amount.data,
                what=self.what.data)
        # set the owers
        for ower in self.payed_for.data:
            bill.owers.append(Person.query.get(ower))

        return bill


class MemberForm(Form):
    def __init__(self, project, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.project = project

    name = TextField("Name", validators=[Required()])
    submit = SubmitField("Add a member")

    def validate_name(form, field):
        if Person.query.filter(Person.name == field.data)\
                .filter(Person.project == form.project).all():
            raise ValidationError("This project already have this member")


class InviteForm(Form):
    emails = TextAreaField("People to notify")
    submit = SubmitField("Send invites")

    def validate_emails(form, field):
        validator = Email()
        for email in [email.strip() for email in form.emails.data.split(",")]:
            if not validator.regex.match(email):
                raise ValidationError("The email %s is not valid" % email)