BROWSER=firefox

install: 
	pipenv install

open-repo:
	${BROWSER} -url "https://github.com/guimassoqueto/scraper-beautiful-soup"