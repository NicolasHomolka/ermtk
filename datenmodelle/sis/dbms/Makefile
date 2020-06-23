# Makefile.rules im Top-Level-Verzeichnis

SUBDIRS := $(wildcard */.)

all: $(SUBDIRS)
$(SUBDIRS):
	-$(MAKE) -C $@

.PHONY: all $(SUBDIRS)
