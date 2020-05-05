from filecmp import cmp
from getpass import getuser
from pathlib import Path
from shutil import copyfile, copytree, rmtree
from socket import socket, AF_UNIX, SOCK_STREAM
from subprocess import Popen, run
from time import sleep

import threading
import unittest


(TRUE, FALSE, BLACK, GREY, WHITE, UNSEEN) = (
    b"true", b"false", b"black", b"grey", b"white", b"unseen")

localconfig = "tmp1/config"
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

greylistcmd = b" --grey 192.0.2.42 send@example.com recv@example.com"


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


def get_value(localconfig, section, key):
    with open(localconfig) as fp:
        for line in fp:
            line = line.strip()

            if line.startswith("#"):
                continue

            if (line[0:1] == '[') and (']' in line):
                _section = line[1:line.find(']')].strip().lower()
                continue

            if ('=' in line):
                _key, _data = [s.strip() for s in line.split('=', 1)]
                if (section == _section) and (_key == key):
                    return _data

    return None


pid = None


class test_basic_checks(unittest.TestCase):
    daemon = None
    sock = None

    def greylistd():
        global pid
        pid = Popen(["program/greylistd", localconfig])

    @classmethod
    def setUpClass(cls):
        rmtree("tmp1", ignore_errors=True)
        Path("tmp1").mkdir(parents=True, exist_ok=True)
        copyfile("tests/config", "tmp1/config")
        with open("tmp1/config", "a") as fp:
            fp.write("owner = %s" % getuser())

        # start the engines
        cls.daemon = threading.Thread(target=cls.greylistd,
                                      name="greylistd",
                                      daemon=True)
        cls.daemon.start()
        cls.sockname = get_value(localconfig, "socket", "path")
        sleep(5)

    @classmethod
    def tearDownClass(cls):
        global pid
        pid.terminate()
        pid.kill()

    def tearDown(self):
        self.sock.close()

    def setUp(self):
        self.sock = socket(AF_UNIX, SOCK_STREAM)
        self.sock.connect(self.sockname)

    def test_first(self):
        self.sock.send(greylistcmd)
        status = self.sock.recv(1024)
        self.assertEqual(status, TRUE, msg="First check.")

    def test_too_fast(self):
        self.sock.send(greylistcmd)
        status = self.sock.recv(1024)
        self.assertEqual(status, TRUE, msg="Retry too fast.")

    def test_white(self):
        sleep(45)
        self.sock.send(greylistcmd)
        status = self.sock.recv(1024)
        self.assertEqual(status, FALSE, msg="Auto whitelist.")


if __name__ == '__main__':
    unittest.main()
