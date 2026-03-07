mypy:
    uvx --with=django-stubs mypy django_urr/

ty:
    uvx --with=django-stubs ty check django_urr/

typecheck: mypy ty
