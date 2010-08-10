**THIS APP IS A WORK IN PROGRESS**. 

See TODO.md

# Example usage

An example project that uses doccomment is included in examples/dc_project. 
To try it out, run:

    $ cd examples/dc_project
    $ export PYTHONPATH='../..'
    $ ./manage.py syncdb
    $ ./manage.py runserver

The project comes with sample sqlite3 db file (data.db) with some prepopulated content. The following users can be used for login:

* **admin** (password: *admin123*) -- has superuser privs
* **author** (password: *author123*) -- can create and publish documents
* **public** (password: *public123*) -- can post comments
* *Anonymous users can only view published documents*

The permission model can be overridden. Documentation to come.

# Dependencies

By default, we use the markdown filter in django.contrib.markup. This
requires:

* python markdown <http://www.freewisdom.org/projects/python-markdown>

We also use the fabulous BeautifulSoup library (included in our distribution)

# Settings

(we need to describe the usage of:)

* DOCCOMMENT_PARSER_MODULE
* DOCCOMMENT_PERMISSION_MODULE
* DOCCOMMENT_MARKDOWN_EXTENSIONS
* DOCCOMMENT_MARKDOWN_SAFEMODE

# Disclaimer

I'm relatively new to Django, so I'm sure there are lots of room for
improvement. 

Feel free to get in touch if you have any comments, suggestions, patches, or
would like to get involved with the project.