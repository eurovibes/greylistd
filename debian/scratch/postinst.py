#!/usr/bin/python
# postinst script for greylistd
#
# see: dh_installdeb(1)
# summary of how this script can be called:
#        * <postinst> `configure' <most-recently-configured-version>
#        * <old-postinst> `abort-upgrade' <new version>
#        * <conflictor's-postinst> `abort-remove' `in-favour' <package>
#          <new-version>
#        * <deconfigured's-postinst> `abort-deconfigure' `in-favour'
#          <failed-install-package> <version> `removing'
#          <conflicting-package> <version>
# for details, see /usr/share/doc/packaging-manual/
#
# quoting from the policy:
#     Any necessary prompting should almost always be confined to the
#     post-installation script, and should be protected with a conditional
#     so that unnecessary prompting doesn't happen if a package's
#     installation fails and the `postinst' is called with `abort-upgrade',
#     `abort-remove' or `abort-deconfigure'.

from debconf import *
from sys     import argv, stderr, exit
from os      import spawnlp, P_WAIT, remove, mkdir, chown
from os.path import exists
from shutil  import move, copy
from pwd     import getpwnam
from grp     import getgrgid


def do_configure (oldversion):
    runFrontEnd()
    db = Debconf()
    
    username = "greylist"
    datadir  = "/var/lib/greylistd"
    rundir   = "/var/run/greylistd"
    docdir   = "/usr/share/doc/greylistd"
    exdir    = docdir + "/examples"
    confdir  = "/etc/greylistd"

    ### If the username does not exist, create it.
    try:
        getpwnam(username)
    except KeyError:
        run("adduser", "--system", "--disabled-password", "--group",
            "--home", datadir, "--no-create-home", username)

    ### Obtain the list of members that should be in the greylist group
    newmembers = db.get("greylistd/users").split()

    ### Find the existing members of the group
    (name, passwd, uid, gid, gecos, dir, shell) = getpwnam(username)
    (groupname, grpasswd, gid, oldmembers) = getgrgid(gid)

    ### Remove any members no longer desired in the group
    for member in oldmembers:
        if not member in members:
            run("deluser", member, groupname)

    ### Add new members to the group
    for member in members:
        if not member in oldmembers:
            run("adduser", member, groupname)

    ### Create and set ownership on directories
    for directory in datadir, rundir:
        if not exists(directory):
            mkdir(directory)
        chown(directory, uid, gid)

    ### Remove obsolete files
    for f in "/etc/default/greylist", "/etc/default/greylistd":
        if exists(f):
            remove(f)

    ### Move any files in old locations to new ones
    for src, dst in ((datadir+"/data", datadir+"/states"),):
        if exists(src) and not exists(dst):
            move(src, dst)


    ### Copy default files into place
    for src, dst in ((exdir+"/whitelist-hosts", confdir+"whitelist-hosts"),):
        if exists(src) and not exists(dst):
            copy(src, dst)



    
def do_reconfigure (oldversion):
    return do_configure(oldversion)


def do_abort_upgrade (newversion):
    pass


def do_abort_remove (infavour, package, newversion):
    pass


def do_abort_deconfigure (infavour, failedpackage, failedversion,
                          removing, conflictpackage, conflictversion):
    pass


def run (command, *args):
    return (spawnlp(P_WAIT, command, command, *args) == 0)


if len(argv) < 2:
    stderr.write("%s: Missing command\n"%(argv[0]))
    exit(1)


name = "do_" + argv[1].lower().replace("-", "_")
args = argv[2:]

try:
    function = globals()[name]
    function(*args)

except KeyError, e:
    stderr.write("%s: Unknown command: %s\n"%(argv[0], argv[1]))
    exit(1)

except TypeError, e:
    stderr.write("%s: %s\n"%(argv[0], e))
    exit(1)

run("update-rc.d", "greylist", "defaults")
run("invoke-rc.d", "greylist", "start")
exit(0)
