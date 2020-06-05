import unittest
import output as o
import sorting as s
import vk


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.account = 553127075
        vk.params['user_id'] = int(self.account)
        self.user_info = vk.get_user_info()
        self.users = vk.search_users(self.user_info)
        self.result = vk.compare_friends_groups(self.users)
        self.top10_users = s.find_top10(self.result)
        self.top10_users_with_photos = vk.find_top3_photos(self.top10_users)
        self.output = o.create_output_file(self.top10_users_with_photos)
    def test_top_3_photos_is_list(self):
        self.assertIsInstance(self.top10_users_with_photos, list)
    def test_output_is_not_empty(self):
        self.assertNotEqual(len(self.output), 0)
        
if __name__ == '__main__':
    unittest.main()

