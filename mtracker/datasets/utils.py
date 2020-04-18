from mtracker.models import Event


def data_query_factory(dset_id: int, data_category: str):
    """
    takes a data category and ID and returns a query
    """
    if data_category == "events":
        return Event.query.filter_by(dataset_id=dset_id)
    else:
        raise ValueError(f"Category {data_category} not found.")


def dset_template_factory(data_category: str) -> str:
    """
    takes a dset category and returns the appropriate template to render
    """
    if data_category == "events":
        return "datasets/event_dataset.html"
