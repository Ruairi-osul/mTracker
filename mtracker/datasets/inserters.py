from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError
import pandas as pd
from mtracker.models import Event


class InsertionError(Exception):
    pass


class Inserter(ABC):
    @abstractmethod
    def _insert(self, data, session):
        pass

    def insert_data(self, data, session):
        try:
            self._insert(data, session)
        except IntegrityError as e:
            print(e)
            raise InsertionError()


class EventInserter(Inserter):
    def _insert(self, data: pd.DataFrame, session) -> None:
        session.bulk_insert_mappings(Event, data.to_dict(orient="records"))
        # data.to_sql(
        # name="events", con=session, index=False, if_exists="append",
        # )


class NeuronsInserter(Inserter):
    def _insert(self, data, session):
        pass


class NeuronalActivityInserter(Inserter):
    def _insert(self, data, session):
        pass


class ContinuousActivityInserter(Inserter):
    def _insert(self, data, session):
        pass


def inserter_factory(category: str):
    if category == "events":
        return EventInserter()
    elif category == "neuronal_activity":
        return NeuronalActivityInserter()
    elif category == "neurons":
        return NeuronsInserter()
    elif category == "continuous":
        return ContinuousActivityInserter()
    else:
        ValueError(f"No known inserter for category {category}")
