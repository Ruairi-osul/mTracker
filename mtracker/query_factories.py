from mtracker.models import Experiment, SessionType, SurgeryType, DataType, Group, Mouse


def experiment_query_factory():
    return Experiment.query


def session_type_factory():
    return SessionType.query


def surgery_type_factory():
    return SurgeryType.query


def data_type_factory():
    return DataType.query


def group_factory():
    return Group.query


def mouse_factory():
    return Mouse.query
