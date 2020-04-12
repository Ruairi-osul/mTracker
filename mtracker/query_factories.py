from mtracker.models import Experiment, SessionType, SurgeryType, DataType


def experiment_query_factory():
    return Experiment.query


def session_type_factory():
    return SessionType.query


def surgery_type_factory():
    return SurgeryType.query


def data_type_factory():
    return DataType.query
