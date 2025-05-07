import unittest

from design_patterns.structural.proxy import PaymentAPI, Proxy, proxy_call


class ProxyTestCase(unittest.TestCase):

    def test_00_init_proxy(self):
        ProxyTestCase.proxy = Proxy(call_limit=3)

    def test_01_test_subject(self):
        api = self.proxy._subject
        self.assertIsInstance(api, PaymentAPI)

    def test_02_test_proxy_call(self):
        call1 = proxy_call(self.proxy, 'bob')
        call2 = proxy_call(self.proxy, 'bob')
        call3 = proxy_call(self.proxy, 'bob')
        call4 = proxy_call(self.proxy, 'bob')

        self.assertEqual(call1, 2)
        self.assertEqual(call2, 1)
        self.assertEqual(call3, 0)
        self.assertEqual(call4, 0)


if __name__ == '__main__':
    unittest.main()
