from pathlib import Path
from typing import Any


def setup_case_folders(case_profile: Any, base_filepaths: list[Path]) -> None:
    """
    Creates the case folder structure based on the case_profile dataclass.
    """
    claimant_name_first = case_profile.claimant_name_first
    claimant_name_last = case_profile.claimant_name_last
    claimant_name_last_initial = case_profile.claimant_name_last_initial
    attorney_name_last = case_profile.attorney_name_last
    attorney_name_first_initial = case_profile.attorney_name_first_initial

    # "Private" claimant folder
    private_econ_folder_dir = base_filepaths[0]
    private_claimant_folder_dir = f"{claimant_name_last_initial}/{claimant_name_last}, {claimant_name_first} ({attorney_name_first_initial}. {attorney_name_last})"
    # THIS IS WHERE I LEFT OFF

    Path.joinpath(private_econ_folder_dir, private_claimant_folder_dir).mkdir(
        parents=True, exist_ok=True
    )

    # "Public" claimant folder
    public_base_dir = base_filepaths[1]
    Path.joinpath(output_base_dir, case_name).mkdir(parents=True, exist_ok=True)
