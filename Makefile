FIREFOX=firefox -url
CHROME=google-chrome


# install all dependencies
install: 
	poetry install

# install pre-commit, update its dependencies and install hook for commit messages
prepare:
	pre-commit install && pre-commit autoupdate && pre-commit install --hook-type commit-msg

# open repo in web browser. Change to CHROME if using google chrome
open-repo:
	${FIREFOX} "https://github.com/guimassoqueto/scraper-beautiful-soup"