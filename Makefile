.DEFAULT_GOAL := all


.PHONY: all
all: format check test version


.PHONY: sync
sync:
	@uv sync --all-extras


.PHONY: help
help: Makefile
	@sed -n 's/^##//p' $< | sort


## upgrade       : Update pre-commit configuration.
.PHONY: upgrade
upgrade: sync
	uv run pre-commit autoupdate


## check         : Execute pre-commit hooks.
.PHONY: check
check: sync
	uv run pre-commit run --all-files


## format        : Format code.
.PHONY: format
format: sync
	uv run ruff format -q .


## test          : Execute tests.
.PHONY: test
test: sync
	uv run pytest -q


## version       : Show which version is detected
.PHONY: version
version: CURRENT:=$(shell uv version --short)
version:
	@echo "Current version: ${CURRENT}"


# release        : Use the value of `NEXT_VERSION` to create new release
.PHONY: release
release: CURRENT:=$(shell uv version --short)
release: test version
	@echo "Next version: ${NEXT_VERSION}"
	@sed  -E -e "s/${CURRENT}/${NEXT_VERSION}/" -i '' README.md pyproject.toml
	@uv lock
	@git add README.md pyproject.toml uv.lock
	git commit -m "chore: release version ${NEXT_VERSION}" && git tag "v${NEXT_VERSION}"


## release-patch : Increase patch version in files, commit and tag with git.
.PHONY: release-patch
release-patch: NEXT_VERSION:=$(shell uv version --dry-run --bump patch --short)
release-patch: release


## release-minor : Increase minor version in files, commit and tag with git.
.PHONY: release-minor
release-minor: NEXT_VERSION:=$(shell uv version --dry-run --bump minor --short)
release-minor: release


## release-major : Increase major version in files, commit and tag with git.
.PHONY: release-major
release-major: NEXT_VERSION:=$(shell uv version --dry-run --bump major --short)
release-major: release
