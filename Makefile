MANAGE=django-admin.py
PROJECT=test_assignment_project
VIRTUALENV_DIR=.env

clean:
	rm -rf build
	rm -rf *~*
	rm -f *.sqlite3
	find . -name '*.pyc' -exec rm {} \;

test: test_core_app test_shell_scripts

test_core_app:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) test core

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) runserver

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) migrate --noinput

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) syncdb --migrate --noinput 

collectstatic:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) \
		collectstatic --noinput

pep8:
	pep8 --filename=*.py --ignore=W --exclude="manage.py,settings.py,urls.py,wsgi.py" --statistics --repeat $(PROJECT) 

pylint:
	pylint $(PROJECT)  --max-public-methods=50 --include-ids=y --ignored-classes=Item.Meta --method-rgx='[a-z_][a-z0-9_]{2,40}$$'

BATS_REPO=https://github.com/sstephenson/bats.git
install_bats:
	if test -f $(VIRTUALENV_DIR)/libexec/bats; then true; \
		else rm -fr tmp; \
			git clone $(BATS_REPO) tmp; \
			exec tmp/install.sh $(VIRTUALENV_DIR); \
	fi;

test_shell_scripts: install_bats
	$(VIRTUALENV_DIR)/libexec/bats project_models_test.bats
