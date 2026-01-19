import unittest
from unittest.mock import MagicMock, patch
from utils.pb_auth import PBAuthManager


class TestPBAuthManager(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://mock-pb:8090"
        self.auth_manager = PBAuthManager(self.base_url)

    @patch("utils.pb_auth.PocketBase")
    def test_get_auth_methods_success(self, MockPocketBase):
        mock_client = MockPocketBase.return_value
        mock_methods = MagicMock()
        mock_client.collection.return_value.list_auth_methods.return_value = (
            mock_methods
        )

        result = self.auth_manager.get_auth_methods()

        self.assertEqual(result, mock_methods)
        mock_client.collection.assert_called_with("users")

    @patch("utils.pb_auth.PocketBase")
    def test_generate_auth_url_success(self, MockPocketBase):
        mock_client = MockPocketBase.return_value

        # Mock provider data
        mock_provider = MagicMock()
        mock_provider.name = "google"
        mock_provider.auth_url = "https://pb.auth/google?redirect="
        mock_provider.code_verifier = "mock_verifier_123"

        mock_methods = MagicMock()
        mock_methods.auth_providers = [mock_provider]
        mock_client.collection.return_value.list_auth_methods.return_value = (
            mock_methods
        )

        redirect_url = "http://localhost:5000/callback"
        result = self.auth_manager.generate_auth_url(redirect_url)

        self.assertIn(
            "https://pb.auth/google?redirect=http://localhost:5000/callback",
            result["authUrl"],
        )
        self.assertEqual(result["codeVerifier"], "mock_verifier_123")
        self.assertEqual(result["provider"], "google")

    @patch("utils.pb_auth.PocketBase")
    def test_authenticate_with_code_success(self, MockPocketBase):
        mock_client = MockPocketBase.return_value
        mock_auth_data = MagicMock()
        mock_client.collection.return_value.auth_with_oauth2.return_value = (
            mock_auth_data
        )

        result = self.auth_manager.authenticate_with_code(
            "code123", "verifier123", "http://callback"
        )

        self.assertEqual(result, mock_auth_data)
        mock_client.collection.assert_called_with("users")
        mock_client.collection.return_value.auth_with_oauth2.assert_called_with(
            "google", "code123", "verifier123", "http://callback"
        )


if __name__ == "__main__":
    unittest.main()
