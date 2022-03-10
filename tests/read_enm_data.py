"""Read the txt files and prepare enm data."""


def read_enm_txt(enm_files):
    """
    Read txt files and return ENM data.

    Args:
        enm_files: list of strings

    Returns:
        list of strings
    """
    enm_results = []
    for enmfile in enm_files:
        file_path = 'tests/enm_data/{enmfile}.txt'.format(enmfile=enmfile)
        with open(file_path) as enm_file_obj:
            enm_data = enm_file_obj.read().split('\n')
            enm_results.append(enm_data)
    return enm_results
