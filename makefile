
make:
	@echo "hello - see readme.md for repo info. run \`make check\` to test repo"

check:
	@./test/test_TspGraph.py
	@./test/test_Environment.py
	@./test/test_WorkerAnt.py
