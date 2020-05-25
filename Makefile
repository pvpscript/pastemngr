PYTHON = $(shell \
	   (python -c "import sys; sys.exit(sys.version >= '3.6'" && \
	    which python) || (which python3)
	   )
ifeq ($(PYTHON),)
	$(error No suitable python found.)
endif
SETUPOPTS = "--record=install_log.txt"
DESTDIR = /
PREFIX = /usr/local
PYOPTIMIZE = 1

clean:
	find pastemngr -regex .*.py[co] -delete
	find pastemngr -depth -name __pycache__ -type d -exec rm -r -- {} \;

install:
	${PYTHON} setup.py install ${SETUPOPTS} \
		--prefix=${PREFIX} --root=${DESTDIR} \
		--optimize=${PYOPTIMIZE}

compile: clean
	PYTHONOPTIMIZE=${PYOPTIMIZE} ${PYTHON} -m compileall -q pastemngr
