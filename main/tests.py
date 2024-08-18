from django.test import TestCase as BaseTestCase


class TestCase(BaseTestCase):

    def setUp(self):
        from django.core.cache import cache

        # Clear all test cache
        cache.clear()
        super().setUp()

    def force_login(self, user):
        self.client.force_login(user)

    def logout(self):
        self.client.logout()

    def assertResponseNoErrors(self, resp, msg=None):
        """
        Assert that the call went through correctly. 200 means the syntax is ok,
        if there are no `errors`,
        the call was fine.
        :resp HttpResponse: Response
        """
        content = resp.json()
        self.assertEqual(resp.status_code, 200, msg or content)
        self.assertNotIn("errors", list(content.keys()), msg or content)

    def assertResponseHasErrors(self, resp, msg=None):
        """
        Assert that the call was failing. Take care: Even with errors,
        GraphQL returns status 200!
        :resp HttpResponse: Response
        """
        content = resp.json()
        self.assertIn("errors", list(content.keys()), msg or content)

    def no_op(*args, **_): ...
