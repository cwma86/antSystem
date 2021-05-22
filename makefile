
make:
	@echo "hello - see readme.md for repo info. run \`make check\` to test repo"

check:
	@./test/TestTspGraph.py
	@./test/TestEnvironment.py
	@./test/TestWorkerAnt.py
