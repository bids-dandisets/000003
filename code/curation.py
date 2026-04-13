import pathlib

def _scrub_tsv_of_line_with_value(tsv_lines: list[str], identifying_values: list[str]) -> list[str]:
    """
    Remove lines containing a specific value from a list of TSV lines.

    Parameters
    ----------
    tsv_lines : list[str]
        The list of lines from a TSV file.
    identifying_values : list[str]
        The value to search for in the lines. Lines containing this value will be removed.

    Returns
    -------
    list[str]
        A new list of lines with the specified value removed.
    """
    corrected_lines = [line for line in tsv_lines if not any(identifying_value in line for identifying_value in identifying_values)]
    return corrected_lines

def _run(dataset_dir: pathlib.Path) -> None:
    dandipaths_with_values_to_fix = {
        "sub-YutaMouse57/ses-YutaMouse57+161010/ecephys/sub-YutaMouse57_ses-YutaMouse57+161010_events.tsv": ["-1596.0487999999987"],
        "sub-YutaMouse42/ses-YutaMouse42+151102/ecephys/sub-YutaMouse42_ses-YutaMouse42+151102_events.tsv": [
            "-7798.642400000001",
            "-9259.1704",
            "-28907.556",
            "-29163.6184",
        ],
    }
    dandipaths_to_local_paths = {
        dandipath: dataset_dir / dandipath
        for dandipath in dandipaths_with_values_to_fix.keys()
    }

    local_paths_with_corrected_values = {
        (path := dandipaths_to_local_paths[dandipath]): _scrub_tsv_of_line_with_value(
            tsv_lines=path.read_text().splitlines(), identifying_values=identifying_values
        )
        for dandipath, identifying_values in dandipaths_with_values_to_fix.items()
    }

    for path, corrected_lines in local_paths_with_corrected_values.items():
        path.write_text("\n".join(corrected_lines))


if __name__ == '__main__':
    dataset_dir = pathlib.Path(__file__).parent.parent
    _run(dataset_dir=dataset_dir)