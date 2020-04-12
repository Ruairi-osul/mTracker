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


group_surgerytypes = db.Table(
    "group_surgerytypes",
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"), primary_key=True),
    db.Column(
        "surgery_id", db.Integer, db.ForeignKey("surgery_types.id"), primary_key=True,
    ),
)


group_sessiontypes = db.Table(
    "group_sessiontypes",
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"), primary_key=True),
    db.Column(
        "sessiontype_id",
        db.Integer,
        db.ForeignKey("session_types.id"),
        primary_key=True,
    ),
)

group_datatypes = db.Table(
    "group_datatypes",
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"), primary_key=True),
    db.Column(
        "datatype_id", db.Integer, db.ForeignKey("data_types.id"), primary_key=True,
    ),
)


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer(), primary_key=True)
    group_name = db.Column(db.String(100))
    genotype = db.Column(db.String(50))
    group_description = db.Column(db.Text)
    experiment_id = db.Column(db.Integer, db.ForeignKey("experiments.id"))

    experiment = db.relationship("Experiment", backref=db.backref("groups"))
    sessions = db.relationship(
        "SessionType", secondary=group_sessiontypes, backref=db.backref("groups")
    )
    surgeries = db.relationship(
        "SurgeryType", secondary=group_surgerytypes, backref=db.backref("groups")
    )
    data_types = db.relationship(
        "DataType", secondary=group_datatypes, backref=db.backref("groups")
    )


class DataType(db.Model):
    __tablename__ = "data_types"
    id = db.Column(db.Integer(), primary_key=True)
    data_name = db.Column(db.String(100))
    data_description = db.Column(db.Text)


class Mouse(db.Model):
    __tablename__ = "mice"
    id = db.Column(db.Integer(), primary_key=True)
    mouse_name = db.Column(db.String(100))
    is_male = db.Column(db.Boolean())
    group_id = db.Column(db.Integer(), db.ForeignKey("groups.id"))
    dob = db.Column(db.Date)
    group = db.relationship("Group", backref=db.backref("mice"))


class HistologyImage(db.Model):
    __tablename__ = "histology"
    # TODO

    mouse = db.relationship("Mouse", backref=db.backref("images"))
    pass
