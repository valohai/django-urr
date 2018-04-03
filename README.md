django-urr
==========

> Django URL resolver utilities

This package aims to make it easier to introspect and possibly manipulate
the URL resolver(s) in Django projects.

We use urr to auto-generate smoke tests for all URLs in the project,
but you might come up with other uses. Who knows!

:point_right: Note that urr is currently only compatible with Django 2+.

Installation
------------

Install the package using `pip install` or similar.

To use the management command(s), also add `django_urr`
to your project's `INSTALLED_APPS`.

`urr_list` Management Command
-----------------------------

You can use the `urr_list` management command to generate
a machine-readable (but human-greppable) list of URLs in your project.

By default, `urr_list` outputs [JSON Lines (`jsonl`)][jsonl], with each
route on a line of its own; this is greppable with standard tools.
If you'd prefer, you can also direct `urr_list` to output a single JSON
array with `--format=json`.

Each route is an object (dict) has the following keys:

* `groups` – the named capture groups (route arguments). 
  For unnamed groups, these are named `_0`, `_1`, etc. by Django.
* `name` – the name of the route, if any
* `namespace` – the namespace of the route, if any
* `path` – the path of the route, as a Python percent format string
* `pattern` – the regex to match the path

Programmatic API
----------------

The `django_urr.extract_urls()` function
traverses the tree of URL patterns and returns an iterator of
`django_urr.extract.URLEntry` objects in original mounting order.

[jsonl]: http://jsonlines.org/
