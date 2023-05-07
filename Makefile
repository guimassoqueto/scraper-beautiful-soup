BROWSER=firefox

install: 
	pipenv install && pipenv shell && pre-commit autoupdate
open-repo:
	${BROWSER} -url "https://github.com/guimassoqueto/scraper-beautiful-soup"