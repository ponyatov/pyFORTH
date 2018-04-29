log.log: src.src FORTH.py
	python FORTH.py $< > $@ && tail $(TAIL) $@
doc:
	doxygen doxy.gen > /dev/null
