# This file is part of PulseAudio.
#
# PulseAudio is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PulseAudio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PulseAudio; if not, see <http://www.gnu.org/licenses/>.

ACLOCAL_AMFLAGS = -I m4

EXTRA_DIST = \
	git-version-gen \
	LICENSE \
	GPL \
	LGPL \
	.gitignore \
	m4/.gitignore \
	src/.gitignore

SUBDIRS = src

MAINTAINERCLEANFILES =
noinst_DATA =

dist-hook:
	echo $(VERSION) > $(distdir)/.tarball-version
	echo $(VERSION) > $(distdir)/.version

.PHONY: homepage distcleancheck doxygen

# see git-version-gen
BUILT_SOURCES = $(top_srcdir)/.version
$(top_srcdir)/.version:
	echo $(VERSION) > $@-t && mv $@-t $@
