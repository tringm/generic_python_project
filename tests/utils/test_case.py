import filecmp
import logging
import time
import unittest
from pathlib import Path
from typing import Optional, Union

from utils.generic_utils import project_root_path


class TestCaseTimer(unittest.TestCase):
    def setUp(self) -> None:
        self._started_at = time.time()

    def tearDown(self) -> None:
        self._elapsed = time.time() - self._started_at


class TestCaseCompare(TestCaseTimer):
    """
    The test case support comparision between the exp file and the out file stored in the output folder of a test case
    """

    @classmethod
    def setUpClass(cls,
                   io_folder_path: Optional[Union[Path, str]] = 'tests/io',
                   in_folder_name: Optional[str] = 'in',
                   out_folder_name: Optional[str] = 'out',
                   test_path: Optional[Union[Path, str]] = None):
        """
        :param io_folder_path: Path to test io folder from project root
        :param in_folder_name: Input folder name
        :param out_folder_name: Output folder name
        :param test_path: Path to test class if specified, else use class name
        :return:
        """
        io_path = project_root_path().joinpath(io_folder_path)
        if not test_path:
            test_path = cls.__name__
        cls.input_folder = (io_path / in_folder_name).joinpath(test_path)
        cls.output_folder = (io_path / out_folder_name).joinpath(test_path)
        cls.output_folder.mkdir(parents=True, exist_ok=True)
        cls.out_file = {}
        cls.exp_file = {}
        cls.in_file = {}

    def setUp(self):
        super().setUp()
        self.method_name = self.id().split('.')[-1]
        self.out_file[self.method_name] = self.output_folder / (self.method_name + '_out.txt')
        self.exp_file[self.method_name] = self.output_folder / (self.method_name + '_exp.txt')
        self.logger = logging.getLogger(self.method_name)

    def file_compare(self, out_f: Path, exp_f: Path, msg=None):
        for f in [out_f, exp_f]:
            if not f.exists():
                raise ValueError(f"{f} does not exist")
            if not f.is_file():
                raise ValueError(f"{f} is not a file")
        if not msg:
            msg = f"{out_f} does not match {exp_f}"
        self.assertTrue(filecmp.cmp(str(out_f), str(exp_f), shallow=False), msg)

    def file_compare_by_method_id(self, method_id):
        self.file_compare(out_f=self.out_file[method_id], exp_f=self.exp_file[method_id])

    def file_compare_default(self):
        method_name = self.id().split('.')[-1]
        self.file_compare(out_f=self.out_file[method_name], exp_f=self.exp_file[method_name])