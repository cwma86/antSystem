
make:
	@echo "hello - see readme.md for repo info. run \`make check\` to test repo"

check:
	@python3 -m unittest discover test/
