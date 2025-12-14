import unittest

from design_patterns.structural.bridge import TV, BridgeRemote, Radio


class BridgeTestCase(unittest.TestCase):

    def test_00_init_bridge(self):
        BridgeTestCase.tv = TV()
        BridgeTestCase.radio = Radio()
        BridgeTestCase.tv_remote = BridgeRemote(self.tv)
        BridgeTestCase.radio_remote = BridgeRemote(self.radio)

    def test_01_test_volume(self):
        tv = TV()
        radio = Radio()
        tv_remote = BridgeRemote(tv, volume_increment=20)
        radio_remote = BridgeRemote(radio, volume_increment=20)

        tv_remote.volume_up()
        radio_remote.volume_down()

        self.assertEqual(tv_remote.device.get_volume(), 70)
        self.assertEqual(radio_remote.device.get_volume(), 30)

    def test_02_test_power(self):
        tv = TV()
        radio = Radio()

        self.assertIs(tv.is_enabled(), False)
        self.assertIs(radio.is_enabled(), False)

        tv_remote = BridgeRemote(tv)
        radio_remote = BridgeRemote(radio)

        tv_remote.toggle_power()
        radio_remote.toggle_power()

        self.assertIs(tv_remote.device.is_enabled(), True)
        self.assertIs(tv_remote.device.is_enabled(), True)

    def test_03_test_channel(self):
        tv = TV()
        radio = Radio()

        self.assertEqual(tv.get_channel(), 1)
        self.assertEqual(radio.get_channel(), 1)

        tv_remote = BridgeRemote(tv)
        radio_remote = BridgeRemote(radio)

        tv_remote.channel_up()
        tv_remote.channel_up()
        tv_remote.channel_up()
        radio_remote.channel_up()
        radio_remote.channel_up()
        radio_remote.channel_down()

        self.assertEqual(tv.get_channel(), 4)
        self.assertEqual(radio.get_channel(), 2)


if __name__ == '__main__':
    unittest.main()
