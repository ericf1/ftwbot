from database.ChannelsDatabase import ChannelsDatabase
from database.SocialDatabase import SocialDatabase
from database.TimeDatabase import TimeDatabase
from database.SettingsDatabase import SettingsDatabase
import unittest
import random
import redis
from redis.commands.json.path import Path
import time


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.supported_platforms = ["instagram", "twitter"]

        cls.social_data = redis.Redis(host='localhost', port=6379, db=4)
        cls.time_data = redis.Redis(host='localhost', port=6379, db=5)
        cls.settings_data = redis.Redis(host='localhost', port=6379, db=6)
        cls.channels_data = redis.Redis(host='localhost', port=6379, db=7)

        cls.social_base = SocialDatabase(4)
        cls.time_base = TimeDatabase(5)
        cls.settings_base = SettingsDatabase(6)
        cls.channels_base = ChannelsDatabase(7)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.social_data.flushdb()
        cls.time_data.flushdb()
        cls.settings_data.flushdb()
        cls.channels_data.flushdb()
        return super().tearDownClass()

    def test_social_data(self):
        self.assertEqual(str(self.social_base.db), str(self.social_data))

        to_be_removed = []
        server_ids = [str(random.randint(100000000, 999999999))
                      for _ in range(5)]

        # for server_id in server_ids:
        #     self.social_base.db.json().set(server_id, Path.root_path(), {})
        for _ in range(5):
            for i, server_id in enumerate(server_ids):
                for platform in self.supported_platforms:
                    self.social_base.add(server_id, platform, f"test{i}")
                    to_be_removed.append([server_id, platform, f"test{i}"])

        test = []
        for server_id in server_ids:
            test.append({server_id: {}})
        for _ in range(5):
            for i, server_id in enumerate(server_ids):
                for platform in self.supported_platforms:
                    if test[i][server_id].get(platform) is None:
                        test[i][server_id][platform] = []
                    test[i][server_id][platform].append(f"test{i}")

        sorted_all = sorted(self.social_base.all,
                            key=lambda d: tuple(d.keys()))
        sorted_test = sorted(test, key=lambda d: tuple(d.keys()))

        self.assertEqual(sorted_all, sorted_test)

        for remove_args in to_be_removed:
            self.social_base.remove(
                remove_args[0], remove_args[1], remove_args[2])

        test = [{server_id: {}} for server_id in server_ids]
        for test_social_data in test:
            for key, value in test_social_data.items():
                for platform in self.supported_platforms:
                    if value.get(platform) is None:
                        test_social_data[key][platform] = []

        sorted_all = sorted(self.social_base.all,
                            key=lambda d: tuple(d.keys()))
        sorted_test = sorted(test, key=lambda d: tuple(d.keys()))

        self.assertEqual(sorted_all, sorted_test)

        database_all = []
        for server_id in server_ids:
            database_all.append({server_id: self.social_base.get(server_id)})
        sorted_all = sorted(self.social_base.all,
                            key=lambda d: tuple(d.keys()))
        sorted_test = sorted(database_all, key=lambda d: tuple(d.keys()))

        self.assertEqual(sorted_all, sorted_test)

    def test_time_data(self):
        self.assertEqual(str(self.time_base.db), str(self.time_data))
        server_ids = [str(random.randint(100000000, 999999999))
                      for _ in range(5)]
        times = [int(time.time()) for _ in range(5)]
        for server_id, timed in zip(server_ids, times):
            self.time_base.db.set(server_id, str(timed))

        test = []
        for server_id, timed in zip(server_ids, times):
            test.append({server_id: str(timed)})

        sorted_all = sorted(self.time_base.all,
                            key=lambda d: tuple(d.keys()))
        sorted_test = sorted(test, key=lambda d: tuple(d.keys()))

        self.assertEqual(sorted_all, sorted_test)

        database_all = []
        for server_id in server_ids:
            database_all.append(
                {server_id: str(self.time_base.get(server_id))})
        sorted_all = sorted(self.time_base.all,
                            key=lambda d: tuple(d.keys()))
        sorted_test = sorted(database_all, key=lambda d: tuple(d.keys()))

        self.assertEqual(sorted_all, sorted_test)

    def test_channels_data(self):
        self.assertEqual(str(self.channels_base.db), str(self.channels_data))

        server_ids = [str(random.randint(100000000, 999999999))
                      for _ in range(5)]
        channel_ids = [[str(random.randint(100000000, 999999999))
                        for _ in range(5)] for _ in range(5)]

        for channel_id, server_id in zip(channel_ids, server_ids):
            for channel in channel_id:
                self.channels_base.add(server_id, channel)

        test = [{server_id: set(channel_id)}
                for channel_id, server_id in zip(channel_ids, server_ids)]

        database_all = self.channels_base.all
        for i, kv in enumerate(database_all):
            for key, value in kv.items():
                database_all[i][key] = set(value)

        sorted_all = sorted(database_all,
                            key=lambda d: tuple(d.keys()))
        sorted_test = sorted(test, key=lambda d: tuple(d.keys()))

        self.assertEqual(sorted_all, sorted_test)

        for channel_id, server_id in zip(channel_ids, server_ids):
            database_from_server_id = set(self.channels_base.get(server_id))
            test_from_server_id = set(channel_id)

            self.assertEqual(database_from_server_id, test_from_server_id)

        for channel_id, server_id in zip(channel_ids, server_ids):
            for channel in channel_id:
                self.channels_base.remove(server_id, channel)

        # self.channels_base.remove(server_ids[0], channel_ids[0][0])
        self.assertEqual(self.channels_base.all, [])

    def test_settings_data(self):
        self.assertEqual(str(self.settings_base.db), str(self.settings_data))
        server_ids = [str(random.randint(100000000, 999999999))
                      for _ in range(5)]

        self.settings_base.add(
            server_ids[0], language="Spanish", send_video_as_link="Yes")

        test = {'language': 'Spanish', 'send_video_as_link': 'Yes'}
        self.assertEqual(self.settings_base.get(server_ids[0]), test)

        test = {"language": "English", "send_video_as_link": "No"}
        self.assertEqual(self.settings_base.get(server_ids[1]), test)


if __name__ == "__main__":
    unittest.main()
