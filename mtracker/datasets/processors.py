from abc import ABC, abstractmethod
import pandas as pd
import os
from pathlib import Path


class ProcessingError(Exception):
    pass


class Processor(ABC):
    @abstractmethod
    def _process_data(self, form_data: str, dset_id: int) -> pd.DataFrame:
        pass

    @staticmethod
    def _save_tmp(file, loc="tmp"):
        tmp_fname = Path(loc)
        tmp_fname.mkdir(exist_ok=True)
        tmp_fname = str(tmp_fname / file.filename)
        file.save(tmp_fname)
        return tmp_fname

    @staticmethod
    def _clean_up(filename):
        os.remove(filename)

    def process_data(self, form_data, dset_id: int) -> pd.DataFrame:
        try:
            tmp_fn = self._save_tmp(form_data)
            df = self._process_data(tmp_fn, dset_id)
            self._clean_up(tmp_fn)
            return df
        except FileNotFoundError:
            raise ProcessingError()


class EventProcessor(Processor):
    def _process_data(self, form_data: str, dset_id: int) -> pd.DataFrame:
        df = pd.read_csv(form_data)
        assert df.columns == ["timepoint_sec"]
        df["dataset_id"] = dset_id
        return df


class NeuronsProcessor(Processor):
    def _process_data(self, form_data: str, dset_id: int) -> pd.DataFrame:
        pass


class NeuronalActivityProcessor(Processor):
    def _process_data(self, form_data: str, dset_id: int) -> pd.DataFrame:
        pass


class ContinuousActivityProcessor(Processor):
    def _process_data(self, form_data: str, dset_id: int) -> pd.DataFrame:
        pass


def processor_factory(category: str):
    if category == "events":
        return EventProcessor()
    elif category == "neuronal_activity":
        return NeuronalActivityProcessor()
    elif category == "neurons":
        return NeuronsProcessor()
    elif category == "continuous":
        return ContinuousActivityProcessor()
    else:
        ValueError(f"No known processors for category {category}")
