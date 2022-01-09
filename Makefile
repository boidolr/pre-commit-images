.DEFAULT_GOAL := all


# venv handling: https://github.com/sio/Makefile.venv/blob/master/Makefile.venv
VENVDIR=.venv
MARKER=.initialized-with-Makefile.venv
VENV=$(VENVDIR)/bin


$(VENV):
	python3 -m venv $(VENVDIR)
	$(VENV)/python3 -m pip install --upgrade pip setuptools wheel


$(VENV)/$(MARKER): $(VENV)


## venv          : Initialize virtual environment with dependencies.
.PHONY: venv
venv: $(VENV)/$(MARKER)
	$(VENV)/pip install -q .[tests]


.PHONY: all
all: format check test version


.PHONY: help
help: Makefile
	@sed -n 's/^##//p' $< | sort


## upgrade       : Update pre-commit configuration.
.PHONY: upgrade
upgrade: venv
	$(VENV)/pre-commit autoupdate


## check         : Execute pre-commit hooks.
.PHONY: check
check: venv
	$(VENV)/pre-commit run --all-files


## format        : Format code.
.PHONY: format
format: venv
	$(VENV)/black -q .


## test          : Execute tests.
.PHONY: test
test: venv
	$(VENV)/pytest -q


## version       : Show which version is detected
CURRENT:=$(subst v,,$(shell git describe --abbrev=0 --tags))
PARTS:=$(subst ., ,$(CURRENT))
MAJOR:=$(word 1, $(PARTS))
MINOR:=$(word 2, $(PARTS))
PATCH:=$(word 3, $(PARTS))
VERSION:=$(MAJOR).$(MINOR).$(PATCH)
.PHONY: version
version:
ifeq "${CURRENT}" "${VERSION}"
	@echo "Current version: ${CURRENT}"
else
	@echo "Version mismatch: ${CURRENT} != ${VERSION}"
endif


# release        : Use the value of `NEXT_VERSION` to create new release
.PHONY: release
release: test version
	@echo "Next version: ${NEXT_VERSION}"
	@sed  -E -e "s/rev: v${CURRENT}/rev: v${NEXT_VERSION}/" -i '' README.md
	@sed  -E -e "s/version = ${CURRENT}/version = ${NEXT_VERSION}/" -i '' setup.cfg
	@git add README.md setup.cfg
	git commit -m "Release version ${NEXT_VERSION}" && git tag "v${NEXT_VERSION}"


## release-patch : Increase patch version in files, commit and tag with git.
.PHONY: release-patch
release-patch: NEXT_VERSION:=${MAJOR}.${MINOR}.$$((${PATCH}+1))
release-patch: release


## release-minor : Increase minor version in files, commit and tag with git.
.PHONY: release-minor
release-minor: NEXT_VERSION:=${MAJOR}.$$((${MINOR}+1)).0
release-minor: release


## release-major : Increase major version in files, commit and tag with git.
.PHONY: release-major
release-major: NEXT_VERSION:=$$((${MAJOR}+1)).0.0
release-major: release


## clean         : Remove virtual environment.
.PHONY: clean
clean:
	rm -r "$(VENVDIR)"
