from .extentions import db


class Experiment(db.Model):
    __tablename__ = "experiments"
    id = db.Column(db.Integer(), primary_key=True)
    exp_name = db.Column(db.String(150))
    exp_description = db.Column(db.Text)


class SessionType(db.Model):
    __tablename__ = "session_types"
    id = db.Column(db.Integer(), primary_key=True)
    session_name = db.Column(db.String(100))
    session_description = db.Column(db.Text)


class SurgeryType(db.Model):
    __tablename__ = "surgery_types"
    id = db.Column(db.Integer(), primary_key=True)
    surgery_name = db.Column(db.String(100))
    surgery_description = db.Column(db.Text)


group_sessiontypes = db.Table(
    "group_sessiontypes",
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"), primary_key=True),
    db.Column("session_types", db.ForeignKey("session_types.id", primary_key=True)),
)

group_surgerytypes = db.Table(
    "group_surgerytypes",
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id", primary_key=True)),
    db.Column(
        "surgery_id", db.Integer, db.ForeignKey("surgery_types.id", primary_key=True)
    ),
)


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
