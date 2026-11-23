import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

import scripts.validate_site as validator


class ValidateSiteTests(unittest.TestCase):
    def test_external_url_is_checked_with_head_request(self):
        response = Mock(status=200)
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        opener = Mock()
        opener.open.return_value = response
        parser = validator.ReferenceParser()

        with patch.object(validator, "build_opener", return_value=opener):
            validator.check_reference(parser, "a", "href", "https://github.com/")

        self.assertEqual(parser.errors, [])
        opener.open.assert_called_once()

    def test_external_url_from_unapproved_host_is_rejected(self):
        parser = validator.ReferenceParser()

        with patch.object(validator, "build_opener") as build_opener:
            validator.check_reference(parser, "a", "href", "https://example.com/")

        self.assertTrue(any("Host externo não permitido" in error for error in parser.errors))
        build_opener.assert_not_called()

    def test_unavailable_external_url_is_rejected(self):
        opener = Mock()
        opener.open.side_effect = HTTPError(
            "https://github.com/",
            404,
            "Not Found",
            hdrs=None,
            fp=None,
        )
        parser = validator.ReferenceParser()

        with patch.object(validator, "build_opener", return_value=opener):
            validator.check_reference(parser, "a", "href", "https://github.com/")

        self.assertTrue(any("HTTP 404" in error for error in parser.errors))


if __name__ == "__main__":
    unittest.main()
