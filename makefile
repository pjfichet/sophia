WHO=sophia
RDM=readme
DOC=utroff-sophia
MAN1=sophia
LIC=bsd2
LOG=log
BIN=philia
STR=philia
CLEAN=bsd2.tr

include ../config.mk ../include.mk

LIBS+=-lsqlite3

.o:
	$(CC) $(LDFLAGS) $< $(LIBS) -o $@

philia: philia.o 
readme.t: ../share/build.tr ../share/bugs.tr
sophia.t: ../share/bugs.tr
utroff-sophia.tr: ../share/info.tr ../share/bsd2.tr readme.tr \
sophia.tr log.tr \
../share/build.tr ../share/bugs.tr

# $Id: makefile,v 0.7 2013/09/09 20:16:04 pj Exp pj $
