# Packaging directory
DESTDIR=
# Prefix directory
PREFIX=/opt/utroff
# Where to place binaries
BINDIR=$(PREFIX)/bin
# Where to place manuals
MANDIR=$(PREFIX)/man

CC = cc
CFLAGS = -Wall -O2 
LDFLAGS =
OBJS = philia.o
LIBS +=-lsqlite3

all: philia
%.o: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) -c $< -o $@

philia: $(OBJS)
	$(CC) $(LDFLAGS) $(OBJS) $(LIBS) -o $@

clean:
	rm -f *.o philia

install:
	test -d $(MANDIR)/man1 || mkdir -p $(MANDIR)/man1
	install -c -m 644 sophia.man $(MANDIR)/man1/sophia.1
	test -d $(BINDIR) || mkdir -p $(BINDIR)
	install -c philia $(BINDIR)/philia
	install -c sophia $(BINDIR)/sophia

uninstall:
	rm -f $(MANDIR)/man1/sophia.1
	rm -f $(BINDIR)/philia
	rm -r $(BINDIR)/sophia
