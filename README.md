**THIS APP IS STILL INCOMPLETE**. See TODO.md

# Example usage

An example project that uses doccomment is included in examples/dc_project. 
To try it out, run:

    $ cd examples/dc_project
    $ export PYTHONPATH='../..'
    $ ./manage.py syncdb
    $ #./manage.py loaddata ???? # Fixture not yet ready
    $ ./manage.py runserver

# Dependencies

By default, we use the markdown filter in django.contrib.markup. This
requires:
* python markdown (http://www.freewisdom.org/projects/python-markdown)

We also use the fabulous BeautifulSoup library (included in our distribution)

# Settings

(we need to describe the usage of:)

DOCCOMMENT_PARSER_MODULE
DOCCOMMENT_PERMISSION_MODULE
DOCCOMMENT_MARKDOWN_EXTENSIONS
DOCCOMMENT_MARKDOWN_SAFEMODE
DOCCOMMENT_DIV_ID_PREFIX


# Disclaimer

I'm relatively new to Django, so I'm sure there will be lots of room for
improvement. 

Feel free to get in touch if you have comments, suggestions, patches, or
would like to get involved with the project.
