# This file is part of PulseAudio.
#
# Copyright 2004-2006 Lennart Poettering
# Copyright 2006 Pierre Ossman <ossman@cendio.se> for Cendio AB
# Copyright 2006 Diego Pettenò
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

###################################
#       Extra directories         #
###################################

###################################
#     Compiler/linker flags       #
###################################

AM_CPPFLAGS = \
	-I$(top_srcdir)/src \
	-I$(top_srcdir)/src/modules \
	-I$(top_builddir)/src/modules \
	-DPA_SRCDIR=\"$(abs_srcdir)\" \
	-DPA_BUILDDIR=\"$(abs_builddir)\" \
	-DPULSE_LOCALEDIR=\"$(localedir)\"
AM_CFLAGS = -std=gnu11 \
	$(PTHREAD_CFLAGS) \
	$(PULSEAUDIO_CFLAGS)

AM_LIBADD = $(PTHREAD_LIBS) $(INTLLIBS) $(PULSEAUDIO_LIBS)
AM_LDFLAGS =
# Should only be applied to libraries.
AM_LIBLDFLAGS = $(NODELETE_LDFLAGS)

if OS_IS_WIN32
AM_LDFLAGS+=-Wl,--export-all-symbols,--enable-auto-import -no-undefined
WINSOCK_LIBS=-lwsock32 -lws2_32 -lwininet
endif

if OS_IS_DARWIN
AM_LDFLAGS+=-Wl,-headerpad_max_install_names -headerpad_max_install_names
endif

FOREIGN_CFLAGS = -w

MODULE_LDFLAGS = $(AM_LDFLAGS) $(AM_LIBLDFLAGS) -module -disable-static -avoid-version $(NOUNDEFINED_LDFLAGS)
MODULE_LIBADD = $(AM_LIBADD)

###################################
#          Includes               #
###################################

BUILT_SOURCES =
CLEANFILES =

###################################
#        Plug-in libraries        #
###################################

modlibexec_LTLIBRARIES = \
		libbluez4-util.la \
		module-bluez4-discover.la \
		module-bluez4-device.la

# Bluetooth BlueZ 4 sink / source
module_bluez4_discover_la_SOURCES = modules/bluetooth/module-bluez4-discover.c
module_bluez4_discover_la_LDFLAGS = $(MODULE_LDFLAGS)
module_bluez4_discover_la_LIBADD = $(MODULE_LIBADD) $(DBUS_LIBS) libbluez4-util.la
module_bluez4_discover_la_CFLAGS = $(AM_CFLAGS) $(DBUS_CFLAGS) -DPA_MODULE_NAME=module_bluez4_discover

libbluez4_util_la_SOURCES = \
		modules/bluetooth/a2dp-codecs.h \
		modules/bluetooth/bluez4-util.c \
		modules/bluetooth/bluez4-util.h
libbluez4_util_la_LDFLAGS = -avoid-version
libbluez4_util_la_LIBADD = $(MODULE_LIBADD) $(DBUS_LIBS)
libbluez4_util_la_CFLAGS = $(AM_CFLAGS) $(DBUS_CFLAGS)

module_bluez4_device_la_SOURCES = modules/bluetooth/module-bluez4-device.c modules/bluetooth/rtp.h
module_bluez4_device_la_LDFLAGS = $(MODULE_LDFLAGS)
module_bluez4_device_la_LIBADD = $(MODULE_LIBADD) $(DBUS_LIBS) $(SBC_LIBS) libbluez4-util.la
module_bluez4_device_la_CFLAGS = $(AM_CFLAGS) $(DBUS_CFLAGS) $(SBC_CFLAGS) -DPA_MODULE_NAME=module_bluez4_device

###################################
#        Some minor stuff         #
###################################

if OS_IS_WIN32
SYMLINK_PROGRAM=cd $(DESTDIR)$(bindir) && cp
else
SYMLINK_PROGRAM=ln -sf
endif
install-exec-hook:
	rm -f $(DESTDIR)$(modlibexecdir)/*.la

uninstall-hook:
	rm -f $(DESTDIR)$(modlibexecdir)/*.so

# Force installation order of libraries. libtool relinks on install time, in
# which case libpulsecommon has to be installed before others, but the padsp
# preload library has to be done after the normal libraries (e.g. libpulse)
# ...
# Unfortunately automake behaviour means that rules without commands also
# override build-in rules, so it's not trivial to add dependencies.
# See http://debbugs.gnu.org/cgi/bugreport.cgi?bug=7328 for the workaround
# ...
# Isn't libtool/autotools fun!

installmodlibexecLTLIBRARIES = install-modlibexecLTLIBRARIES

.PHONY: massif update-all update-ffmpeg update-map-file coverage
