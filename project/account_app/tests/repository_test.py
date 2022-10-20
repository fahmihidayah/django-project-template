from .base_setup_test import AccountBaseSetupTestCase
from account_app.repositories import UserRepository


class RepositoryTestCase(AccountBaseSetupTestCase):

    def setUp(self) -> None:
        super(RepositoryTestCase, self).setUp()
        self.user_repository : UserRepository = UserRepository()

    def test_find_by_id_true(self):
        selected_user = self.user_repository.find_by_id(id=self.user.pk)
        self.assertIsNotNone(selected_user)
    #
    # def test_find_by_id_profile_not_none_true(self):
    #     with self.assertNumQueries(2):
    #         selected_user = self.user_repository.find_by_id(id=self.user.pk)
    #         self.assertIsNotNone(selected_user.profile)
    #
    #
    # def test_find_by_id_query_one(self):
    #     with self.assertNumQueries(2):
    #         selected_user = self.user_repository.find_by_id(id=self.user.pk)
    #         self.assertIsNotNone(selected_user.company_set.count())


