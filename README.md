Master Branch: [![Build Status](https://travis-ci.com/eurovibes/greylistd.svg?branch=master)](https://travis-ci.com/eurovibes/greylistd)

# greylistd

Greylisting daemon for use with Exim 4

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes
on how to deploy the project on a live system.

### Prerequisites

Use [Debian GNU/Linux](https://www.debian.org/) :smile:


### Installing

You just want to use greylistd?
Just install it from your next debian mirror...

```
apt-get install greylistd
```

You want to get involved in development?

1. Install build dependencies:
  - debhelper
  - dh-python
  - git-buildpackage
  - python3

  ```
  $ sudo apt-get install debhelper dh-python git-buildpackage python3
  ```

2. Build the package
  ```
  $ gbp buildpackage -uc -us
  ```
3. Start development

## Running the tests

**greylistd** use the python
[unit testing framework](https://docs.python.org/3/library/unittest.html) for
testing. Further informations about the framework can be found there.

You can run the tests by performing
```
$ python3 -m unittest discover -vv -s tests/
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/eurovibes/greylistd/tags).

## greylistd licensing rules

greylistd is provided under the terms of the GNU General Public License
version 2 or later (GPL-2.0-or-later).
The licenses is provided in LICENSES/GPL-2.0.

This documentation file provides a description of how each source file should
be annotated to make its license clear and unambiguous. It doesn’t replace the
greylistd license.

The common way of expressing the license of a source file is to add the
matching boilerplate text into the top comment of the file. Due to formatting,
typos etc. these “boilerplates” are hard to validate for tools which are used
in the context of license compliance.

An alternative to boilerplate text is the use of Software Package Data
Exchange (SPDX) license identifiers in each source file. SPDX license
identifiers are machine parsable and precise shorthands for the license under
which the content of the file is contributed. SPDX license identifiers are
managed by the SPDX Workgroup at the Linux Foundation and have been agreed on
by partners throughout the industry, tool vendors, and legal teams. For
further information see https://spdx.org/

greylistd requires the precise SPDX identifier in all source files. The valid
identifiers used in greylistd are explained in the section License
identifiers and have been retrieved from the official SPDX license list at
https://spdx.org/licenses/ along with the license texts.

### License identifier syntax

1. Placement:
The SPDX license identifier in greylistd files shall be added at the first
possible line in a file which can contain a comment. For the majority of files
this is the first line, except for scripts which require the
‘#!PATH_TO_INTERPRETER’ in the first line. For those scripts the SPDX
identifier goes into the second line.

2. Style:
The SPDX license identifier is added in form of a comment. The comment style
depends on the file type:

```
C source: // SPDX-License-Identifier: <SPDX License Expression>
C header: /* SPDX-License-Identifier: <SPDX License Expression> */
scripts:  # SPDX-License-Identifier: <SPDX License Expression>
```

If a specific tool cannot handle the standard comment style, then the
appropriate comment mechanism which the tool accepts shall be used. This is
the reason for having the “/* */” style comment in C header files. There was
build breakage observed with generated .lds files where ‘ld’ failed to parse
the C++ comment. This has been fixed by now, but there are still older
assembler tools which cannot handle C++ style comments.

3. Syntax:
A <SPDX License Expression> is an SPDX short form license identifier found on
the SPDX License List.

### License identifiers
The licenses currently used, as well as the licenses for code added to
greylistd, is GPL-2.0.

The license is available from the directory:

```
LICENSES/
```

in the greylistd source tree.

The files in this directory contain the full license text and Metatags. The
file names are identical to the SPDX license identifier which shall be used
for the license in source files.
Examples:

```
LICENSES/GPL-2.0
```

Contains the GPL version 2 license text and the required metatags.

Metatags:
The following meta tags must be available in a license file:

* Valid-License-Identifier:
One or more lines which declare which License Identifiers are valid inside the
project to reference this particular license text. Usually this is a single
valid identifier.

* SPDX-URL:
The URL of the SPDX page which contains additional information related to the
license.

* Usage-Guidance:
Freeform text for usage advice. The text must include correct examples for the
SPDX license identifiers as they should be put into source files according to
the License identifier syntax guidelines.

* License-Text:
All text after this tag is treated as the original license text
File format examples:

```
Valid-License-Identifier: GPL-2.0
Valid-License-Identifier: GPL-2.0+
SPDX-URL: https://spdx.org/licenses/GPL-2.0.html
Usage-Guide:
  To use this license in source code, put one of the following SPDX
  tag/value pairs into a comment according to the placement
  guidelines in the licensing rules documentation.
  For 'GNU General Public License (GPL) version 2 only' use:
    SPDX-License-Identifier: GPL-2.0
  For 'GNU General Public License (GPL) version 2 or any later version' use:
    SPDX-License-Identifier: GPL-2.0-or-later
License-Text:
  Full license text
```

## Authors

* **Tor Slettnes** - *He did the initial work*
* **Thorsten Alteholz**
* **Julien Danjou**
* **Dominic Hargreaves**
* **Christian Perrier**
* **Benedikt Spranger**
* **Matthew Wakeling**

See also the list of [contributors](https://github.com/eurovibes/greylistd/contributors) who participated in this project.
