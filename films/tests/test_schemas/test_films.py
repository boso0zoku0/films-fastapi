import string
from unittest import TestCase

from pydantic import ValidationError

from schemas.film import Films, FilmsCreate, FilmsRead, FilmsUpdate, FilmsUpdatePartial


class FilmsTestCase(TestCase):
    def test_film_can_be_created_from_create_scheme(self) -> None:
        film_in = FilmsCreate(
            name="Matrix",
            slug="matrix",
            description="Is film Matrix",
            year_release=2000,
        )

        film = Films(**film_in.model_dump())

        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)

    def test_film_can_be_created_from_update_scheme(self) -> None:
        film_in = FilmsUpdate(
            name="Matrix",
            description="Is film Matrix",
            year_release=2000,
        )

        film = Films(**film_in.model_dump())

        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)

    def test_empty_movie_can_be_created_from_partial_update_scheme(self) -> None:
        film_in = FilmsUpdatePartial(
            name=None,
            description=None,
            year_release=None,
        )
        film = FilmsUpdatePartial(**film_in.model_dump())
        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)

    def test_partially_filled_film_can_be_created_from_the_partial_update_scheme(
        self,
    ) -> None:
        film_in = FilmsUpdatePartial(
            name="Matrix",
            description=None,
            year_release=1999,
        )
        film = FilmsUpdatePartial(**film_in.model_dump())
        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)


class FilmsComplicatedTestCase(TestCase):

    def test_films_create_accepts_different_urls(self) -> None:
        names = [
            "Qweasd",
            "ZxcAsdQweQweAsd",
            "ZXC",
        ]

        for name in names:
            with self.subTest(name=name, msg=f"added name: {name}"):
                film_in = FilmsCreate(
                    name=name,
                    slug="qweabc",
                    description="Is new film",
                    year_release=1999,
                )
                self.assertEqual(
                    name.rstrip("/"),
                    film_in.model_dump(mode="json")["name"].rstrip("/"),
                )

    def test_films_update_accepts_different_urls(self) -> None:
        names = ["Matrix", "maTriX", "Clan @Soprano", " dw цв"]

        for name in names:
            with self.subTest(name=names, msg=f"new name: {name}"):
                film_in = FilmsUpdate(
                    name=name,
                    description="Is new film",
                    year_release=1999,
                )
                self.assertEqual(name, film_in.model_dump(mode="json")["name"])

    def test_films_slug_too_long(self) -> None:

        with self.assertRaises(ValidationError):
            FilmsCreate(
                name="test_film",
                slug="qweabdsfc",
                description="This string contains more than thirty alphabetic characters.",
                year_release=1999,
            )

    def test_films_create_slug_long_film_with_regex(self) -> None:

        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at most 300 characters",
        ) as exc_info:
            FilmsCreate(
                name="test_film",
                slug="qweabc",
                description="Cooper /Matthew McConaughey/ is a spaceship pilot who went on an expedition "
                "to find new planets for life, where humanity can move from the dying Earth.Cooper "
                "/Matthew McConaughey/ is a spaceship pilot who went on an expedition to find "
                "new planets for life, where humanity can move from the dying Earth. Cooper /Matthew "
                "McConaughey/ is a spaceship pilot who went on an expedition "
                "to find new planets for life, where humanity can move from the dying Earth.Cooper "
                "/Matthew McConaughey/ is a spaceship pilot who went on an expedition to find "
                "new planets for life, where humanity can move from the dying Earth.",
                year_release=1999,
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_long"
        self.assertEqual(expected_type, error_details["type"])

    def test_films_error(self) -> None:
        data_film_read = FilmsRead(
            name="dwqwd",
            slug="dwqwd",
            description="Is new film",
            year_release=1999,
        )
        with self.assertRaisesRegex(
            AssertionError,
            expected_regex="'dwqwd' != 'dwqwdabcdefghijklmnopqrstuvwxyz'",
        ):
            data_films = Films(**data_film_read.model_dump())
            expected_film = data_films.name
            result = data_film_read.name + "".join(string.ascii_lowercase)
            self.assertEqual(expected_film, result)
