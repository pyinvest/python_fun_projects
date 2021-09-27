from main import move_folder, get_all_filenames, create_folders, move_files
import pytest
import random
import os
from pathlib import Path


class TestOrganize:
    def setup_method(self):
        self.test_folder = r"C:\Users\p3000\workspace\python_fun_projects\folder_organize\test_folder"  # noqa: E501
        test_path = Path(self.test_folder)
        self.test_paper_path = test_path / "papers_or_book"
        number_of_files = 15

        choices = [
            ".epub", '.pdf', ".jpeg", ".png", ".mp4", ".mov", ".zip", ".rar"
        ]
        self.papers = []
        self.pics = []
        self.videos = []
        self.zipped = []
        self.filenames = []
        for n in range(number_of_files):
            file_type = random.choice(choices)
            filename = "test" + str(n) + file_type
            if file_type in [".epub", ".pdf"]:
                self.papers.append(filename)
            elif file_type in [".jpeg", ".png"]:
                self.pics.append(filename)
            elif file_type in [".mp4", ".mov"]:
                self.videos.append(filename)
            elif file_type in [".zip", ".rar"]:
                self.zipped.append(filename)
            self.filenames.append(filename)
            with open(test_path / filename, 'w'):
                pass

    def test_move_folder(self):
        move_folder(self.test_folder)
        assert os.getcwd() == self.test_folder
        wrong_folder = r"C:\Users\Jenny_Tasi"
        with pytest.raises(Exception) as exc_info:
            move_folder(wrong_folder)
        exception_raised = exc_info.value
        assert "The folder does not exist" == str(exception_raised)

    def test_get_all_filenames(self):
        move_folder(self.test_folder)
        filenames = get_all_filenames()
        assert len(filenames) == len(self.filenames)
        for filename in filenames:

            assert filename in self.filenames

    def test_move_papers(self):
        current_path = Path(self.test_folder)
        filenames = self.filenames
        create_folders(current_path)
        move_files(current_path, filenames)
        test_paper_path = self.test_paper_path
        for paper in self.papers:
            paper_file_path = test_paper_path / paper
            assert os.path.isfile(paper_file_path)

    def teardown_method(self):
        test_path = Path(self.test_folder)
        papers_folder_path = test_path / 'papers_or_book'
        pics_folder_path = test_path / 'pictures'
        video_folder_path = test_path / 'videos'
        zipped_folder_path = test_path / 'zipped'

        for filename in self.filenames:
            if os.path.isfile(test_path / filename):
                os.remove(test_path / filename)

        for paper_file in self.papers:
            if os.path.isfile(papers_folder_path / paper_file):
                os.remove(papers_folder_path / paper_file)

        for pic_file in self.pics:
            if os.path.isfile(pics_folder_path / pic_file):
                os.remove(pics_folder_path / pic_file)

        for video_file in self.videos:
            if os.path.isfile(video_folder_path / video_file):
                os.remove(video_folder_path / video_file)

        for zip_file in self.zipped:
            if os.path.isfile(zipped_folder_path / zip_file):
                os.remove(zipped_folder_path / zip_file)
