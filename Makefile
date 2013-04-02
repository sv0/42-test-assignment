MANAGE=django-admin.py
PROJECT=test_assignment_project

clean:
	rm -rf build
	rm -rf *~*
	rm -f *.sqlite3
	find . -name '*.pyc' -exec rm {} \;

test: clean
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) test core

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) runserver

migrate: syncdb
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) migrate --noinput

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) syncdb --noinput 

collectstatic:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) \
		collectstatic --noinput

pep8:
	pep8 --filename=*.py --ignore=W --exclude="manage.py,settings.py,urls.py,wsgi.py" --statistics --repeat $(PROJECT) 

pylint:
	pylint $(PROJECT)  --max-public-methods=50 --include-ids=y --ignored-classes=Item.Meta --method-rgx='[a-z_][a-z0-9_]{2,40}$$'

