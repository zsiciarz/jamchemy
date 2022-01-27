# --- prologue ---
#
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
.DELETE_ON_ERROR:
.ONESHELL:

# --- variables ---

project_name := jamchemy
python_version := 3.10.1
python_bin := $(HOME)/.pyenv/versions/$(python_version)/bin/python

# Check if we have an external virtualenv (like one created with
# virtualenvwrapper). If so, we should use that one.
check_external_virtualenv := $(shell test -d "$(WORKON_HOME)/$(project_name)" && echo $$?)
ifneq ($(check_external_virtualenv), 0)
$(shell test -d .venv || $(python_bin) -m venv .venv)
virtualenv_path := .venv
else
virtualenv_path := $(WORKON_HOME)/$(project_name)
endif

virtualenv_pip := $(virtualenv_path)/bin/pip
virtualenv_python := $(virtualenv_path)/bin/python
virtualenv_uvicorn := $(virtualenv_path)/bin/uvicorn
virtualenv_precommit := $(virtualenv_path)/bin/pre-commit

# --- targets ---

.PHONY: help run check
.DEFAULT_GOAL := help

help: ## Show this help and exit
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.test_requirements.sentinel: requirements.txt test_requirements.txt
	$(virtualenv_pip) install pip --upgrade
	$(virtualenv_pip) install -r test_requirements.txt
	touch $@

run: .test_requirements.sentinel ## Run ASGI server
	$(virtualenv_uvicorn) --app-dir=src app:app

check: .test_requirements.sentinel ## Run linters and style checkers
	$(virtualenv_precommit) run --all-files
