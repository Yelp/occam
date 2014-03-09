.PHONY: clean test tests

test:
	testify tests

tests: test

clean:
	find . -name '*.pyc' -delete
