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
## Authors

* **Tor Slettnes** - *He did the initial work*
* **Thorsten Alteholz**
* **Julien Danjou**
* **Dominic Hargreaves**
* **Christian Perrier**
* **Benedikt Spranger**
* **Matthew Wakeling**

See also the list of [contributors](https://github.com/eurovibes/greylistd/contributors) who participated in this project.
