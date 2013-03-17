# A BSD-compatible install command.
INSTALL=/usr/bin/install

# Packaging prefix.
ROOT=

# PREFIX directory
PREFIX=

# Where to place binaries.
BINDIR=$(PREFIX)/bin

# Where to place libraries.
LIBDIR=$(PREFIX)/lib

# Where to place manual pages.
MANDIR=$(PREFIX)/man

# Binaries are stripped with this command after installation.
STRIP=strip -s -R .comment -R .note

# The C compiler.
CC=cc

# Compiler flags.
CFLAGS=-O

# C preprocessor flags.
# Use -D_GNU_SOURCE for Linux with GNU libc.
# Use -D_INCLUDE__STDC_A1_SOURCE for HP-UX.
CPPFLAGS=-D_GNU_SOURCE

# Warning flags for the compiler.
#WARN=

# Linker flags.
LDFLAGS=

# Additional libraries to link with.
LIBS=


OBJ=philia.o

FLAGS=$(EUC) -DLIBDIR='"$(LIBDIR)"'

.SUFFIXES: .man .1

.c.o:
	$(CC) $(CFLAGS) $(WARN) $(FLAGS) $(CPPFLAGS) -c $<

philia: philia.o
	$(CC) $(LDFLAGS) philia.o $(LIBS) -o $@


.man.1:
	sed -e "s|@BINDIR@|$(BINDIR)|g" $< > $@

MAN=
BIN=philia
man: $(MAN)
bin: $(BIN)
all: bin man



installbin: bin
	test -d $(ROOT)$(BINDIR) || mkdir -p $(ROOT)$(BINDIR)
	for f in $(BIN); do \
		$(INSTALL) -c $$f $(ROOT)$(BINDIR)/$$f; \
		$(STRIP) $(ROOT)$(BINDIR)/$$f; \
	done

installman: man
	test -d $(ROOT)$(MANDIR)/man1 || mkdir -p $(ROOT)$(MANDIR)/man1/
	for f in $(MAN); do \
		$(INSTALL) -c -m 644 $$f $(ROOT)$(MANDIR)/man1/$$f; \
	done

install: installbin installman

uninstall:
	cd $(ROOT)$(BINDIR)/ && rm -f $(BIN)
	cd $(ROOT)$(MANDIR)/man1/ && rm -f $(MAN)

clean:
	rm -f $(OBJ) $(BIN) $(MAN)

mrproper: clean

# $Id$
