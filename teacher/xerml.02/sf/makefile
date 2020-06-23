.PHONY: validate

XML = sf.bug.xerml.xml
PDF = $(XML).pdf
GRAMMAR = ../bin/xerml.rnc
SEED = 4

all: validate $(PDF)

validate:
	jing -c $(GRAMMAR) $(XML)

$(PDF): $(XML)
	../bin/xerml2gv $(XML) $(SEED)
