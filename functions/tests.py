import unittest
from get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_directory_outside_working_directory(self):
        expected = (
            "Result for '/bin' directory:\n"
            "Error: Cannot list '/bin' as it is outside the permitted working directory"
        )

        result = get_files_info("calculatoor", "/bin")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
