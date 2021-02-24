# -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

# This file is part of PulseAudio.
#
# Copyright 2004-2008 Lennart Poettering
# Copyright 2006-2007 Pierre Ossman <ossman@cendio.se> for Cendio AB
#
# PulseAudio is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
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

AC_PREREQ(2.63)

AC_INIT([pulseaudio],[m4_esyscmd(./git-version-gen .tarball-version)],[pulseaudio-discuss (at) lists (dot) freedesktop (dot) org],[pulseaudio],[http://pulseaudio.org/])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_AUX_DIR([build-aux])
AM_INIT_AUTOMAKE([foreign 1.11 -Wall -Wno-portability subdir-objects silent-rules color-tests dist-xz tar-ustar])

AS_IF([! test -n "$VERSION"], [
   AC_MSG_ERROR([git-version-gen failed])
])

m4_define(pa_major, `echo $VERSION | cut -d. -f1 | cut -d- -f1`)
m4_define(pa_minor, `echo $VERSION | cut -d. -f2 | cut -d- -f1`)

AC_SUBST(PA_MAJOR, pa_major)
AC_SUBST(PA_MINOR, pa_minor)
AC_SUBST(PA_MAJORMINOR, pa_major.pa_minor)

AC_CANONICAL_HOST
AC_DEFINE_UNQUOTED([CANONICAL_HOST], "$host", [Canonical host string.])

AC_CHECK_PROG([STOW], [stow], [yes], [no])

AS_IF([test "x$STOW" = "xyes" && test -d /usr/local/stow], [
    AC_MSG_NOTICE([*** Found /usr/local/stow: default install prefix set to /usr/local/stow/${PACKAGE_NAME}-${PACKAGE_VERSION} ***])
    ac_default_prefix="/usr/local/stow/${PACKAGE_NAME}-${PACKAGE_VERSION}"
])

AM_SILENT_RULES([yes])


#### Checks for programs. ####

# mkdir -p

AC_PROG_MKDIR_P

# ln -s

AC_PROG_LN_S

# CC

AC_PROG_CC
AM_PROG_CC_C_O

# M4

AC_CHECK_PROGS([M4], gm4 m4, no)
AS_IF([test "x$M4" = "xno"], AC_MSG_ERROR([m4 missing]))

#### Determine host OS ####

# if the host has the possibility of sys/capability.h for dropping privileges
# used to determine if we should error out if it is not found
host_has_caps=0

os_is_linux=0
os_is_win32=0
os_is_darwin=0

AC_MSG_CHECKING([host operating system])
case "$host_os" in
    linux*)
        AC_MSG_RESULT([linux])
        host_has_caps=1
        os_is_linux=1
    ;;
    freebsd*)
        AC_MSG_RESULT([freebsd])
        host_has_caps=1
    ;;
    netbsd*)
        AC_MSG_RESULT([netbsd])
    ;;
    darwin*)
        AC_MSG_RESULT([darwin])
        os_is_darwin=1
        AC_DEFINE([OS_IS_DARWIN], 1, [Build target is Darwin.])
    ;;
    mingw*)
        AC_MSG_RESULT([win32])
        os_is_win32=1
        AC_DEFINE([OS_IS_WIN32], 1, [Build target is Windows.])
    ;;
    *)
        AC_MSG_RESULT([unknown])
    ;;
esac

AM_CONDITIONAL(OS_IS_DARWIN, test "x$os_is_darwin" = "x1")
AM_CONDITIONAL(OS_IS_WIN32, test "x$os_is_win32" = "x1")
AC_SUBST([OS_IS_WIN32], [$os_is_win32])

# Platform specific hacks
case "$host_os" in
    darwin* )
        AC_DEFINE([_DARWIN_C_SOURCE], [200112L], [Needed to get NSIG on Mac OS X])
    ;;
    mingw* )
        AC_DEFINE([WIN32_LEAN_AND_MEAN], 1, [Needed to avoid including unnecessary headers on Windows])
    ;;
    solaris* )
        AC_DEFINE(_XOPEN_SOURCE,       600, [Needed to get declarations for msg_control and msg_controllen on Solaris])
        AC_DEFINE(__EXTENSIONS__,        1, [Needed to get declarations for msg_control and msg_controllen on Solaris])
    ;;
esac


#### Compiler flags ####

AX_CHECK_COMPILE_FLAG([-std=gnu11],
   [],
   [AC_MSG_ERROR([*** Compiler does not support -std=gnu11])],
   [-pedantic -Werror])

AX_APPEND_COMPILE_FLAGS(
    [-Wall -W -Wextra -pipe -Wno-long-long -Wno-overlength-strings -Wunsafe-loop-optimizations -Wundef -Wformat=2 -Wlogical-op -Wsign-compare -Wformat-security -Wmissing-include-dirs -Wformat-nonliteral -Wold-style-definition -Wpointer-arith -Winit-self -Wdeclaration-after-statement -Wfloat-equal -Wmissing-prototypes -Wstrict-prototypes -Wredundant-decls -Wmissing-declarations -Wmissing-noreturn -Wshadow -Wendif-labels -Wcast-align -Wstrict-aliasing -Wwrite-strings -Wno-unused-parameter -ffast-math -fno-common -fdiagnostics-show-option -fdiagnostics-color=auto],
    [], [-pedantic -Werror])

AS_CASE([" $CFLAGS "], [*" -O0 "*], [], [
    # Don't append the flag if it already exists.
    # Only enable fastpath asserts when doing a debug build, e.g. from bootstrap.sh.
    AX_APPEND_FLAG([-DFASTPATH], [CPPFLAGS])

    # Cannot use AX_APPEND_FLAG here, as it assumes no space inside the added flags.
    # Cannot append flags with AX_APPEND_FLAG one by one, as this would destroy all fortifications
    # if CPPFLAGS already contain -D_FORTIFY_SOURCE=2.

    # Warnings to be aware of that appear with -D_FORTIFY_SOURCE=2 but without -U_FORTIFY_SOURCE:
    # On Fedora 20 with -O0: #warning _FORTIFY_SOURCE requires compiling with optimization (-O) [-Wcpp]
    # On Gentoo with -O2:    "_FORTIFY_SOURCE" redefined [enabled by default]
    AS_VAR_APPEND([CPPFLAGS],[" -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2"])
])

#### Linker flags ####

# Check whether the linker supports the -version-script option.
# The Make variable $(srcdir) needs to be in the LDFLAGS in that form,
# so that it is expanded the right way in every subdir.
AX_CHECK_LINK_FLAG(["-Wl,-version-script=${srcdir}/src/map-file"],
    [VERSIONING_LDFLAGS='-Wl,-version-script=$(abs_top_srcdir)/src/map-file'])
AC_SUBST([VERSIONING_LDFLAGS])

# Use immediate (now) bindings; avoids the funky re-call in itself.
# The -z now syntax is lifted from Sun's linker and works with GNU's too, other linkers might be added later.
AX_APPEND_LINK_FLAGS([-Wl,-z,now], [IMMEDIATE_LDFLAGS])
AC_SUBST([IMMEDIATE_LDFLAGS])
AS_CASE([$IMMEDIATE_LDFLAGS],[*-z,now*],
    [AC_DEFINE([HAVE_BIND_NOW],[1],
               [Define to 1 if immediate binding is available])])

# On ELF systems we don't want the libraries to be unloaded since we don't clean them up properly,
# so we request the nodelete flag to be enabled.
# On other systems, we don't really know how to do that, but it's welcome if somebody can tell.
AX_APPEND_LINK_FLAGS([-Wl,-z,nodelete], [NODELETE_LDFLAGS], [-shared])
AC_SUBST([NODELETE_LDFLAGS])

# Check for the proper way to build libraries that have no undefined symbols
case $host in
    # FreeBSD (et al.) does not complete linking for shared objects when pthreads
    # are requested, as different implementations are present.
    *-freebsd* | *-openbsd*) ;;
    *)
        for possible_flag in "-Wl,--no-undefined" "-Wl,-z,defs"; do
            AX_CHECK_LINK_FLAG([$possible_flag], [NOUNDEFINED_LDFLAGS="$possible_flag"; break])
        done
    ;;
esac
AC_SUBST([NOUNDEFINED_LDFLAGS])


#### Atomic operations ####

# Native atomic operation support
AC_ARG_ENABLE([atomic-arm-linux-helpers],
    AS_HELP_STRING([--disable-atomic-arm-linux-helpers],[use inline asm or libatomic_ops instead]))

AC_ARG_ENABLE([atomic-arm-memory-barrier],
    AS_HELP_STRING([--enable-atomic-arm-memory-barrier],[only really needed in SMP arm systems]))

if test "x$enable_atomic_arm_memory_barrier" = "xyes"; then
    AC_DEFINE_UNQUOTED(ATOMIC_ARM_MEMORY_BARRIER_ENABLED, 1, [Enable memory barriers])
fi

# If everything else fails use libatomic_ops
need_libatomic_ops=yes

AC_CACHE_CHECK([whether $CC knows __sync_bool_compare_and_swap()],
    pulseaudio_cv_sync_bool_compare_and_swap, [
    AC_LINK_IFELSE(
        [AC_LANG_PROGRAM([], [[int a = 4; __sync_bool_compare_and_swap(&a, 4, 5);]])],
        [pulseaudio_cv_sync_bool_compare_and_swap=yes],
        [pulseaudio_cv_sync_bool_compare_and_swap=no])
    ])

if test "$pulseaudio_cv_sync_bool_compare_and_swap" = "yes" ; then
    AC_DEFINE([HAVE_ATOMIC_BUILTINS], 1, [Have __sync_bool_compare_and_swap() and friends.])
    need_libatomic_ops=no
else
    # HW specific atomic ops stuff
    AC_MSG_CHECKING([architecture for native atomic operations])
    case $host in
        *-netbsd*)
            AC_MSG_RESULT([yes])
            need_libatomic_ops=no
        ;;
        arm*)
            AC_MSG_RESULT([arm])
            AC_MSG_CHECKING([whether we can use Linux kernel helpers])
            # The Linux kernel helper functions have been there since 2.6.16. However
            # compile time checking for kernel version in cross compile environment
            # (which is usually the case for arm cpu) is tricky (or impossible).
            if test "x$os_is_linux" = "x1" && test "x$enable_atomic_arm_linux_helpers" != "xno"; then
                AC_MSG_RESULT([yes])
                AC_DEFINE_UNQUOTED(ATOMIC_ARM_LINUX_HELPERS, 1, [special arm linux implementation])
                need_libatomic_ops=no
            else
                AC_MSG_RESULT([no])
                AC_CACHE_CHECK([compiler support for arm inline asm atomic operations],
                    pulseaudio_cv_support_arm_atomic_ops, [
                    AC_COMPILE_IFELSE(
                        [AC_LANG_PROGRAM([], [[
                            volatile int a=0;
                            int o=0, n=1, r;
                            asm volatile ("ldrex    %0, [%1]\n"
                                          "subs  %0, %0, %2\n"
                                          "strexeq %0, %3, [%1]\n"
                                          : "=&r" (r)
                                          : "r" (&a), "Ir" (o), "r" (n)
                                          : "cc");
                            return (a==1 ? 0 : -1);
                        ]])],
                        [pulseaudio_cv_support_arm_atomic_ops=yes],
                        [pulseaudio_cv_support_arm_atomic_ops=no])
                ])
                AS_IF([test "$pulseaudio_cv_support_arm_atomic_ops" = "yes"], [
                    AC_DEFINE([ATOMIC_ARM_INLINE_ASM], 1, [Have ARM atomic instructions.])
                    need_libatomic_ops=no
                ])
            fi
        ;;
        *-freebsd*)
            AC_MSG_RESULT([yes])
            need_libatomic_ops=no
        ;;
        *)
            AC_MSG_RESULT([unknown])
        ;;
    esac
fi

# If we're on ARM, check for the ARMV6 instructions we need */
case $host in
  arm*)
    AC_CACHE_CHECK([support for required armv6 instructions],
      pulseaudio_cv_support_armv6,
      [AC_COMPILE_IFELSE(
         [AC_LANG_PROGRAM([],
           [[volatile int a = -60000, b = 0xaaaabbbb, c = 0xccccdddd;
             asm volatile ("ldr r0, %2 \n"
                           "ldr r2, %3 \n"
                           "ldr r3, %4 \n"
                           "ssat r1, #8, r0 \n"
                           "str r1, %0 \n"
                           "pkhbt r1, r3, r2, LSL #8 \n"
                           "str r1, %1 \n"
                           : "=m" (a), "=m" (b)
                           : "m" (a), "m" (b), "m" (c)
                           : "r0", "r1", "r2", "r3", "cc");
             return (a == -128 && b == 0xaabbdddd) ? 0 : -1;
           ]])],
         [pulseaudio_cv_support_armv6=yes],
         [pulseaudio_cv_support_armv6=no])
      ])
    AS_IF([test "$pulseaudio_cv_support_armv6" = "yes"], [
        AC_DEFINE([HAVE_ARMV6], 1, [Have ARMv6 instructions.])
      ])
  ;;
  *)
  ;;
esac

#### NEON optimisations ####
AC_ARG_ENABLE([neon-opt],
    AS_HELP_STRING([--enable-neon-opt], [Enable NEON optimisations on ARM CPUs that support it]))

AS_IF([test "x$enable_neon_opt" != "xno"],
    [save_CFLAGS="$CFLAGS"; CFLAGS="-mfpu=neon $CFLAGS"
     AC_COMPILE_IFELSE(
        [AC_LANG_PROGRAM([[#include <arm_neon.h>]], [])],
        [
         HAVE_NEON=1
         NEON_CFLAGS="-mfpu=neon"
        ],
        [
         HAVE_NEON=0
         NEON_CFLAGS=
        ])
     CFLAGS="$save_CFLAGS"
    ],
    [HAVE_NEON=0])

AS_IF([test "x$enable_neon_opt" = "xyes" && test "x$HAVE_NEON" = "x0"],
      [AC_MSG_ERROR([*** Compiler does not support -mfpu=neon or CFLAGS override -mfpu])])

AC_SUBST(HAVE_NEON)
AC_SUBST(NEON_CFLAGS)
AM_CONDITIONAL([HAVE_NEON], [test "x$HAVE_NEON" = x1])
AS_IF([test "x$HAVE_NEON" = "x1"], AC_DEFINE([HAVE_NEON], 1, [Have NEON support?]))


#### libtool stuff ####

LT_PREREQ(2.4)
LT_INIT([dlopen win32-dll disable-static])

dnl As an extra safety device, check for lt_dladvise_init() which is
dnl only implemented in libtool 2.x, and refine as we go if we have
dnl refined requirements.
dnl
dnl Check the header files first since the system may have a
dnl libltdl.so for runtime, but no headers, and we want to bail out as
dnl soon as possible.
dnl
dnl We don't need any special variable for this though, since the user
dnl can give the proper place to find libltdl through the standard
dnl variables like LDFLAGS and CPPFLAGS.

AC_CHECK_HEADER([ltdl.h],
    [AC_CHECK_LIB([ltdl], [lt_dladvise_init], [LIBLTDL=-lltdl], [LIBLTDL=])],
    [LIBLTDL=])

AS_IF([test "x$LIBLTDL" = "x"],
    [AC_MSG_ERROR([Unable to find libltdl version 2. Makes sure you have libtool 2.4 or later installed.])])
AC_SUBST([LIBLTDL])


###################################
#   Basic environment checks      #
###################################

#### Checks for header files. ####

# ISO
AC_HEADER_STDC

# POSIX
AC_CHECK_HEADERS_ONCE([arpa/inet.h cpuid.h glob.h grp.h netdb.h netinet/in.h \
    netinet/in_systm.h netinet/tcp.h poll.h pwd.h sched.h \
    sys/mman.h sys/select.h sys/socket.h sys/wait.h \
    sys/uio.h syslog.h sys/dl.h dlfcn.h linux/sockios.h])
AC_CHECK_HEADERS([netinet/ip.h], [], [],
                 [#include <sys/types.h>
                  #if HAVE_NETINET_IN_H
                  # include <netinet/in.h>
                  #endif
                  #if HAVE_NETINET_IN_SYSTM_H
                  # include <netinet/in_systm.h>
                  #endif
                 ])
AC_CHECK_HEADERS([sys/resource.h], [HAVE_SYS_RESOURCE_H=1], [HAVE_SYS_RESOURCE_H=0])
AC_SUBST(HAVE_SYS_RESOURCE_H)
AC_CHECK_HEADERS([sys/un.h], [HAVE_AF_UNIX=1], [HAVE_AF_UNIX=0])
AM_CONDITIONAL(HAVE_AF_UNIX, test "x$HAVE_AF_UNIX" = "x1")
AC_SUBST(HAVE_AF_UNIX)

# Linux
AC_CHECK_HEADERS([linux/input.h], [HAVE_EVDEV=1], [HAVE_EVDEV=0])
AM_CONDITIONAL([HAVE_EVDEV], [test "x$HAVE_EVDEV" = "x1"])

AC_CHECK_HEADERS_ONCE([sys/prctl.h])

# Solaris
AC_CHECK_HEADERS_ONCE([sys/conf.h sys/filio.h])

# Windows
AC_CHECK_HEADERS_ONCE([windows.h winsock2.h ws2tcpip.h])

# NetBSD
AC_CHECK_HEADERS_ONCE([sys/atomic.h])

# Other
AC_CHECK_HEADERS_ONCE([sys/ioctl.h])
AC_CHECK_HEADERS_ONCE([byteswap.h])
AC_CHECK_HEADERS_ONCE([sys/syscall.h])
AC_CHECK_HEADERS_ONCE([sys/eventfd.h])
AC_CHECK_HEADERS_ONCE([execinfo.h])
AC_CHECK_HEADERS_ONCE([langinfo.h])
AC_CHECK_HEADERS_ONCE([regex.h pcreposix.h])
AC_CHECK_HEADERS_ONCE([locale.h xlocale.h])

AM_CONDITIONAL(HAVE_SYS_EVENTFD_H, test "x$ac_cv_header_sys_eventfd_h" = "xyes")

#### Typdefs, structures, etc. ####

AC_C_CONST
AC_C_BIGENDIAN
AC_TYPE_PID_T
AC_TYPE_SIZE_T
AC_CHECK_TYPES(ssize_t, , AC_DEFINE([ssize_t], [signed long], [Define ssize_t if it is not done by the standard libs.]))
AC_TYPE_OFF_T

AC_TYPE_UID_T
AC_CHECK_DECLS(environ)

AC_CHECK_SIZEOF(void*)

fast_64bit_operations="no"
# This check covers x32-ABI
AC_CHECK_DECL([__x86_64__], [fast_64bit_operations="yes"], [], [])
if test "x$fast_64bit_operations" = "xno"; then
    AS_IF([test $ac_cv_sizeof_voidp -ge 8], [fast_64bit_operations="yes"])
fi

AS_IF([test "x$fast_64bit_operations" = "xyes"], AC_DEFINE([HAVE_FAST_64BIT_OPERATIONS], 1, [Have CPU with fast 64-bit operations?]))

# SIGXCPU
AX_CHECK_DEFINE([signal.h], [SIGXCPU], [HAVE_SIGXCPU=1], [HAVE_SIGXCPU=0])
AS_IF([test "x$HAVE_SIGXCPU" = "x1"], AC_DEFINE([HAVE_SIGXCPU], 1, [Have SIGXCPU?]))
AM_CONDITIONAL(HAVE_SIGXCPU, test "x$HAVE_SIGXCPU" = "x1")

# INADDR_NONE, Solaris lacks this
AX_CHECK_DEFINE([netinet/in.h], [INADDR_NONE], [],
    [AX_CHECK_DEFINE([winsock2.h], [INADDR_NONE], [],
        [AC_DEFINE([INADDR_NONE],  [0xffffffff], [Define INADDR_NONE if not found in <netinet/in.h>])])])


# _Bool
AC_CACHE_CHECK([whether $CC knows _Bool],
    pulseaudio_cv__Bool,
    [AC_COMPILE_IFELSE(
        [AC_LANG_PROGRAM([], [[_Bool b;]])],
        [pulseaudio_cv__Bool=yes],
        [pulseaudio_cv__Bool=no])
    ])

AS_IF([test "$pulseaudio_cv__Bool" = "yes"], AC_DEFINE([HAVE_STD_BOOL], 1, [Have _Bool.]))


#### Check for libs ####

# ISO
AC_SEARCH_LIBS([pow], [m])

# POSIX
AC_SEARCH_LIBS([sched_setscheduler], [rt])
AC_SEARCH_LIBS([dlopen], [dl])
AC_SEARCH_LIBS([shm_open], [rt])
AC_SEARCH_LIBS([inet_ntop], [nsl])
AC_SEARCH_LIBS([timer_create], [rt])
AC_SEARCH_LIBS([pthread_setaffinity_np], [pthread])
AC_SEARCH_LIBS([pthread_getname_np], [pthread])
AC_SEARCH_LIBS([pthread_setname_np], [pthread])

# BSD
AC_SEARCH_LIBS([connect], [socket])
AC_SEARCH_LIBS([backtrace], [execinfo ubacktrace])

# Darwin/OS X
if test "x$os_is_darwin" = "x1" ; then
    AC_MSG_CHECKING([looking for Apple CoreService Framework])
    AC_CHECK_HEADER([CoreServices/CoreServices.h],
        [LIBS="$LIBS -framework CoreServices"],
        [AC_MSG_ERROR([CoreServices.h header file not found])]
    )

    AC_MSG_RESULT([ok])
    AC_DEFINE([HAVE_CLOCK_GETTIME], 1, [Using clock_gettime() replacement])
    HAVE_BONJOUR=1
fi

AM_CONDITIONAL([HAVE_BONJOUR], [test "x$HAVE_BONJOUR" = x1])

# Windows
AC_SEARCH_LIBS([regexec], [pcreposix])
# This magic is needed so we do not needlessly add static libs to the win32  build, disabling its ability to make dlls.
AC_CHECK_FUNCS([getopt_long], [], [AC_CHECK_LIB([iberty], [getopt_long])])


#### Check for functions ####

# ISO
AC_CHECK_FUNCS_ONCE([lrintf strtof])

# POSIX
AC_FUNC_FORK
AC_FUNC_GETGROUPS
AC_CHECK_FUNCS_ONCE([chmod chown fstat fchown fchmod clock_gettime getaddrinfo getgrgid_r getgrnam_r \
    getpwnam_r getpwuid_r gettimeofday getuid mlock nanosleep \
    pipe posix_fadvise posix_madvise posix_memalign setpgid setsid shm_open \
    sigaction sleep symlink sysconf uname pthread_setaffinity_np pthread_getname_np pthread_setname_np])
AC_CHECK_FUNCS([mkfifo], [HAVE_MKFIFO=1], [HAVE_MKFIFO=0])
AC_SUBST(HAVE_MKFIFO)
AM_CONDITIONAL(HAVE_MKFIFO, test "x$HAVE_MKFIFO" = "x1")

# X/OPEN
AC_CHECK_FUNCS_ONCE([readlink])

# SUSv2
AC_CHECK_FUNCS_ONCE([ctime_r usleep])

# SUSv3
AC_CHECK_FUNCS_ONCE([strerror_r])

# BSD
AC_CHECK_FUNCS_ONCE([lstat paccept])

# Non-standard
AC_CHECK_FUNCS_ONCE([setresuid setresgid setreuid setregid seteuid setegid ppoll strsignal sig2str strtod_l pipe2 accept4])

AC_FUNC_ALLOCA

AC_CHECK_FUNCS([regexec], [HAVE_REGEX=1], [HAVE_REGEX=0])
AM_CONDITIONAL(HAVE_REGEX, [test "x$HAVE_REGEX" = "x1"])

# Large File-Support (LFS)
AC_SYS_LARGEFILE
# Check for open64 to know if the current system does have open64() and similar functions
AC_CHECK_FUNCS_ONCE([open64])

AC_SEARCH_LIBS([dladdr], [dl], [HAVE_DLADDR=1], [HAVE_DLADDR=0])
AC_DEFINE(HAVE_DLADDR, [1], [Have dladdr?])

###################################
#      External libraries         #
###################################

#### atomic-ops ####

AC_MSG_CHECKING([whether we need libatomic_ops])
if test "x$need_libatomic_ops" = "xyes"; then
    AC_MSG_RESULT([yes])
    AC_CHECK_HEADERS([atomic_ops.h],
        [CFLAGS="$CFLAGS -DAO_REQUIRE_CAS"],
        [AC_MSG_ERROR([*** libatomic-ops headers not found])])

    # Win32 does not need the lib and breaks horribly if we try to include it
    AS_IF([test "x$os_is_win32" != "x1"], [LIBS="$LIBS -latomic_ops"])
else
    AC_MSG_RESULT([no])
fi

PKG_CHECK_MODULES([PULSEAUDIO], [libpulse >= 12.2 pulsecore >= 12.2 ])
AC_SUBST(PULSEAUDIO_CFLAGS)
AC_SUBST(PULSEAUDIO_LIBS)

#### D-Bus support (optional) ####

AC_ARG_ENABLE([dbus],
    AS_HELP_STRING([--disable-dbus],[Disable optional D-Bus support]))

AS_IF([test "x$enable_dbus" != "xno"],
    [PKG_CHECK_MODULES(DBUS, [ dbus-1 >= 1.4.12 ], HAVE_DBUS=1, HAVE_DBUS=0)],
    HAVE_DBUS=0)

AS_IF([test "x$enable_dbus" = "xyes" && test "x$HAVE_DBUS" = "x0"],
    [AC_MSG_ERROR([*** D-Bus not available or too old version])])

AS_IF([test "x$HAVE_DBUS" = "x1"],
    [
        save_CFLAGS="$CFLAGS"; CFLAGS="$CFLAGS $DBUS_CFLAGS"
        save_LIBS="$LIBS"; LIBS="$LIBS $DBUS_LIBS"
        AC_CHECK_FUNCS(dbus_watch_get_unix_fd)
        CFLAGS="$save_CFLAGS"
        LIBS="$save_LIBS"
    ])

AC_SUBST(HAVE_DBUS)
AM_CONDITIONAL([HAVE_DBUS], [test "x$HAVE_DBUS" = x1])
AS_IF([test "x$HAVE_DBUS" = "x1"], AC_DEFINE([HAVE_DBUS], 1, [Have D-Bus.]))

PA_MACHINE_ID="${sysconfdir}/machine-id"
AX_DEFINE_DIR(PA_MACHINE_ID, PA_MACHINE_ID, [D-Bus machine-id file])
PA_MACHINE_ID_FALLBACK="${localstatedir}/lib/dbus/machine-id"
AX_DEFINE_DIR(PA_MACHINE_ID_FALLBACK, PA_MACHINE_ID_FALLBACK,
	      [Fallback machine-id file])

#### BlueZ support (optional, dependent on D-Bus and SBC) ####

AC_ARG_ENABLE([bluez4],
    AS_HELP_STRING([--disable-bluez4],[Disable optional BlueZ 4 support]))
AC_ARG_ENABLE([bluez5],
    AS_HELP_STRING([--disable-bluez5],[Disable optional BlueZ 5 support]))

## SBC ##
AS_IF([test "x$enable_bluez4" != "xno" || test "x$enable_bluez5" != "xno"],
    [PKG_CHECK_MODULES(SBC, [ sbc >= 1.0 ], HAVE_SBC=1, HAVE_SBC=0)],
    HAVE_SBC=0)

## BlueZ 4 ##
AS_IF([test "x$enable_bluez4" != "xno" && test "x$HAVE_DBUS" = "x1" && test "x$HAVE_SBC" = "x1"], HAVE_BLUEZ_4=1,
      HAVE_BLUEZ_4=0)
AS_IF([test "x$enable_bluez4" = "xyes" && test "x$HAVE_BLUEZ_4" != "x1"],
    [AC_MSG_ERROR([*** BLUEZ 4 support not found (requires sbc and D-Bus)])])
AC_SUBST(HAVE_BLUEZ_4)
AM_CONDITIONAL([HAVE_BLUEZ_4], [test "x$HAVE_BLUEZ_4" = x1])

#### Build and Install man pages ####

AC_ARG_ENABLE([manpages],
    AS_HELP_STRING([--disable-manpages],[Disable building and installation of man pages]))

AM_CONDITIONAL([BUILD_MANPAGES], [test "x$enable_manpages" != "xno"])

#### Thread support ####

AX_TLS
AS_IF([test "$ac_cv_tls" = "__thread"],
    AC_DEFINE([SUPPORT_TLS___THREAD], 1, [Define this if the compiler supports __thread for Thread-Local Storage]))

# Win32 build breaks with win32 pthread installed
AS_IF([test "x$os_is_win32" != "x1"],
  [AX_PTHREAD])

AS_IF([test "x$ax_pthread_ok" = "xyes"],
    AC_DEFINE([_POSIX_PTHREAD_SEMANTICS], 1, [Needed on Solaris]))



###################################
#            Output               #
###################################

AC_DEFINE_UNQUOTED(PA_CFLAGS, "$CFLAGS", [The CFLAGS used during compilation])

AC_ARG_WITH(
        [module-dir],
        AS_HELP_STRING([--with-module-dir],[Directory where to install the modules to (defaults to ${libdir}/pulse-${PA_MAJORMINOR}/modules]),
        [modlibexecdir=$withval], [modlibexecdir="${libdir}/pulse-${PA_MAJORMINOR}/modules"])

AC_SUBST(modlibexecdir)
AX_DEFINE_DIR(PA_DLSEARCHPATH, modlibexecdir, [Modules dir])


AC_CONFIG_FILES([
Makefile
src/Makefile
])

AC_OUTPUT

# ==========================================================================

AS_IF([test "x$HAVE_DBUS" = "x1"], ENABLE_DBUS=yes, ENABLE_DBUS=no)
AS_IF([test "x$HAVE_BLUEZ_4" = "x1"], ENABLE_BLUEZ_4=yes, ENABLE_BLUEZ_4=no)

echo "
 ---{ $PACKAGE_NAME $VERSION }---

    prefix:                        ${prefix}
    modlibexecdir:                 ${modlibexecdir}
    Compiler:                      ${CC}
    CFLAGS:                        ${CFLAGS}
    CPPFLAGS:                      ${CPPFLAGS}
    LIBS:                          ${LIBS}

    Enable D-Bus:                  ${ENABLE_DBUS}
      Enable BlueZ 4:              ${ENABLE_BLUEZ_4}
"
