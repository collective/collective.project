test:
	flake8 collective/project/*.py
	flake8 collective/project/browser/*.py
	flake8 collective/project/tests/*.py
	check-manifest
	pyroma .
	viewdoc
