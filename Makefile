

.PHONY: test
test:
	PYTHONPATH=`pwd` python3 -m pytest test/unit/ -vv
