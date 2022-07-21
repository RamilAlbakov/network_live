"""Add physical parameters to cell object."""


def add_physical_params(atoll_data, cell_obj):
    """
    Add physical parameters to cell object.

    Args:
        atoll_data: dict
        cell_obj: dict

    Returns:
        dict
    """
    try:
        physical_params = atoll_data[cell_obj['cell_name']]
    except KeyError:
        physical_params = {
            'azimut': None,
            'height': None,
            'longitude': None,
            'latitude': None,
        }
    return {**cell_obj, **physical_params}
