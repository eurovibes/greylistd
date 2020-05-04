from filecmp import cmp
from shutil import copytree, rmtree
from subprocess import run

import unittest

setuphelper = "program/greylistd-setup-exim4"
add_split_data = [setuphelper, "add", "-no-reload",
                  "tmp/40_exim4-config_check_data", "acl_check_data"]
del_split_data = [setuphelper, "remove", "-no-reload",
                  "tmp/40_exim4-config_check_data", "acl_check_data"]
add_split_rcpt = [setuphelper, "add", "-no-reload",
                  "tmp/30_exim4-config_check_rcpt", "acl_check_rcpt"]
del_split_rcpt = [setuphelper, "remove", "-no-reload",
                  "tmp/30_exim4-config_check_rcpt", "acl_check_rcpt"]

add_combined_data = [setuphelper, "add", "-no-reload",
                     "tmp/exim4.conf.template", "acl_check_data"]
del_combined_data = [setuphelper, "remove", "-no-reload",
                     "tmp/exim4.conf.template", "acl_check_data"]
add_combined_rcpt = [setuphelper, "add", "-no-reload",
                     "tmp/exim4.conf.template", "acl_check_rcpt"]
del_combined_rcpt = [setuphelper, "remove", "-no-reload",
                     "tmp/exim4.conf.template", "acl_check_rcpt"]

class test_setup_exim4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Copy test data
        rmtree("tmp", ignore_errors=True)
        copytree("tests/data", "tmp")

    def test_data_single(self):
        result = run(add_split_data)
        self.assertEqual(result.returncode, 0,
                         "Fail to add data ACLs to split configuration file.")
        self.assertTrue(cmp("tmp/40_exim4-config_check_data",
                            "tests/data/40_exim4-config_check_data_patched",
                            shallow=False))

        result = run(del_split_data)
        self.assertEqual(result.returncode, 0,
                         "Fail to del data ACLs from split configuration file.")
        self.assertTrue(cmp("tmp/40_exim4-config_check_data",
                            "tests/data/40_exim4-config_check_data",
                            shallow=False))

    def test_rcpt_single(self):
        result = run(add_split_rcpt)
        self.assertEqual(result.returncode, 0,
                         "Fail to add data ACLs to split configuration file.")
        self.assertTrue(cmp("tmp/30_exim4-config_check_rcpt",
                            "tests/data/30_exim4-config_check_rcpt_patched",
                            shallow=False))

        result = run(del_split_rcpt)
        self.assertEqual(result.returncode, 0,
                         "Fail to del data ACLs from split configuration file.")
        self.assertTrue(cmp("tmp/30_exim4-config_check_rcpt",
                            "tests/data/30_exim4-config_check_rcpt",
                            shallow=False))

    def test_combined(self):
        result = run(add_combined_data)
        self.assertEqual(result.returncode, 0,
                         "Fail to add data ACLs to combined configuration file.")

        result = run(add_combined_rcpt)
        self.assertEqual(result.returncode, 0,
                         "Fail to add data ACLs to combined configuration file.")
        self.assertTrue(cmp("tmp/exim4.conf.template",
                            "tests/data/exim4.conf.template_patched",
                            shallow=False))

        result = run(del_combined_data)
        self.assertEqual(result.returncode, 0,
                         "Fail to del data ACLs from combined configuration file.")

        result = run(del_combined_rcpt)
        self.assertEqual(result.returncode, 0,
                         "Fail to del data ACLs from combined configuration file.")
        self.assertTrue(cmp("tmp/exim4.conf.template",
                            "tests/data/exim4.conf.template",
                            shallow=False))

if __name__ == '__main__':
    unittest.main()
