import unittest
import ipaddress
import ip


class FirstDifOctetCase(unittest.TestCase):
    def test_equal_addresses(self):
        expected = None
        actual = ip.first_dif_octet(ipaddress.ip_address('198.125.145.34'), ipaddress.ip_address('198.125.145.34'))
        self.assertEqual(actual, expected)

    def test_boundary_values(self):
        expected = 3
        actual = ip.first_dif_octet(ipaddress.ip_address('198.125.145.34'), ipaddress.ip_address('198.125.145.00'))
        self.assertEqual(actual, expected)


class OctetMaskLenCase(unittest.TestCase):
    def test_equal_octets(self):
        expected = None
        actual = ip.octet_mask_len(198, 198)
        self.assertEqual(actual, expected)

    def test_boundary_values(self):
        expected = 7
        actual = ip.octet_mask_len(128, 129)
        self.assertEqual(actual, expected)


class FindSubnetCase(unittest.TestCase):
    def test_equal_addresses(self):
        expected = ipaddress.ip_network('198.125.145.34/32')
        actual = ip.find_subnet(ipaddress.ip_address('198.125.145.34'), ipaddress.ip_address('198.125.145.34'))
        self.assertEqual(actual, expected)

    def test_opposite_addresses(self):
        expected = ipaddress.ip_network('0.0.0.0/0')
        actual = ip.find_subnet(ipaddress.ip_address('0.0.0.1'), ipaddress.ip_address('255.255.255.255'))
        self.assertEqual(actual, expected)

    def test_diff_addresses(self):
        expected = ipaddress.ip_network('192.0.0.0/2')
        actual = ip.find_subnet(ipaddress.ip_address('198.168.123.1'), ipaddress.ip_address('255.255.255.255'))
        self.assertEqual(actual, expected)

    def test_usual_addresses(self):
        expected = ipaddress.ip_network('77.45.208.0/22')
        actual = ip.find_subnet(ipaddress.ip_address('77.45.208.34'), ipaddress.ip_address('77.45.211.12'))
        self.assertEqual(actual, expected)


class FindMinSubnetCase(unittest.TestCase):
    def test_empty(self):
        expected = None
        actual = ip.find_min_subnet([])
        self.assertEqual(actual, expected)

    def test_one(self):
        expected = ipaddress.ip_network('77.45.208.34/32')
        actual = ip.find_min_subnet([ipaddress.ip_address('77.45.208.34')])
        self.assertEqual(actual, expected)

    def test_equals(self):
        expected = ipaddress.ip_network('77.45.208.34/32')
        actual = ip.find_min_subnet([
            ipaddress.ip_address('77.45.208.34'),
            ipaddress.ip_address('77.45.208.34'),
            ipaddress.ip_address('77.45.208.34')
        ])
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
