DEV_PYTHON_VER ?= 3.11

BIN ?= build/bin

ENVS ?= envs

CONDA ?= micromamba
CONDA_ACTIVATE ?= eval "$$(micromamba shell hook --shell=bash)" && micromamba activate
CHANNEL ?= defaults

DEV_ENV = $(ENVS)/py$(DEV_PYTHON_VER)

USE_ROSETTA = true

ifeq ($(USE_ROSETTA), true)
  ifeq ($(shell uname -p),arm)
    CONDA := CONDA_SUBDIR=osx-64 $(CONDA)
  endif
endif

shell: $(DEV_ENV)
	$(CONDA_ACTIVATE) $(DEV_ENV) && bash --init-file .init-file.bash

$(ENVS)/py%:
	$(CONDA) create -y -c $(CHANNEL) -p $@ "python=$*"
	mkdir -p $(BIN)
	ln -fs $(abspath $@/bin/python$*) $(BIN)/

clean:

realclean: clean
	$(RM) -r build
	$(RM) -r envs

.PHONY: clean realclean
