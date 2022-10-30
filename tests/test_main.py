import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch
import main

class TestMain(TestCase):
    @patch('main.getenv', MagicMock())
    @patch('main.OAuth2Session', MagicMock(return_value=MagicMock(fetch_token=(MagicMock(return_value={'foo': 'bar'})))))
    @patch('main.datastore.Client')
    @patch('main.datastore.Entity')
    def test_token_returned_by_oauth_added_to_datastore(self, entity_cls, client_cls):
        put_method = MagicMock()
        client = MagicMock(put=put_method)
        client_cls.return_value = client
        update_method = MagicMock()
        entity = MagicMock(update=update_method)
        entity_cls.return_value = entity

        main.execute(None)

        update_method.assert_called_with({'foo': 'bar'})
        put_method.assert_called_with(entity)
