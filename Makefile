GITPACK_VERSION := $(shell git rev-list --full-history --all --abbrev-commit | head -1)
all:
	docker build -t h42-gaming/console:latest -t h42-gaming/console:$(GITPACK_VERSION) ./frontend-game
