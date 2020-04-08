from .extentions import db


class Experiment(db.Model):
    __tablename__ = "experiments"
    id = db.Column(db.Integer(), primary_key=True)
    exp_name = db.Column(db.String(150))
    exp_description = db.Column(db.Text)


class SessionType(db.Model):
    __tablename__ = "session_types"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer(), primary_key=True)
    group_name = db.Column(db.String(100))
    genotype = db.Column(db.String(50))
    group_description = db.Column(db.Text)


class Mouse(db.Model):
    __tablename__ = "mice"
    id = db.Column(db.Integer(), primary_key=True)
    mouse_name = db.Column(db.String(100))
    is_male = db.Column(db.Boolean())
    group_id = db.Column(db.Integer(), db.ForeignKey("groups.id"))
    dob = db.Column(db.Date)
    group = db.relationship("Group", backref=db.backref("mice", lazy="dynamic"))
