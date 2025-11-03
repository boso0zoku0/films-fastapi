from unittest import TestCase

from dependencies.auth import UNSAFE_METHODS
from dependencies.films import GetFilmsStorage, prefetch_url_film
from storage.films.crud import storage


class DependsTestCase(TestCase):

    def test_prefetch_url_film(self) -> None:
        slugs = {su.slug for su in storage.get()}
        for slug in slugs:
            prefetch_url_film(slug=slug, storage=storage)


class TestUnsafeMethods(TestCase):
    def test_unsafe_methods_doesnt_contain_safe_methods(self) -> None:
        safe_methods = {"GET", "OPTIONS", "HEAD"}
        assert not UNSAFE_METHODS & safe_methods

    def test_uppercase_unsafe_methods(self) -> None:
        assert all(method.isupper() for method in UNSAFE_METHODS)
