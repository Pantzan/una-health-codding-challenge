from pathlib import Path


def get_sample_csv_file(file: str) -> bytes:
    """
    Hackish way to navigate into una/assets directory and return the file read in memory

    :param: file: the filename to be read
    """

    project_root_directory = Path(__file__).parents[2]
    assets_directory = Path(project_root_directory / "sample_data")
    first_sample_data = Path(assets_directory / file)

    with open(str(first_sample_data), 'rb') as csv_file:
        csv_file_content = csv_file.read()

    return csv_file_content
