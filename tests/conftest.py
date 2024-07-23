import pytest
import os
import shutil
from gaboon.project.project_class import Project

from .base_test import COUNTER_PROJECT_PATH


@pytest.fixture
def gaboon_project():
    return Project(COUNTER_PROJECT_PATH)


@pytest.fixture
def cleanup_out_folder():
    yield
    created_folder_path = COUNTER_PROJECT_PATH.joinpath("out/")
    if os.path.exists(created_folder_path):
        shutil.rmtree(created_folder_path)
