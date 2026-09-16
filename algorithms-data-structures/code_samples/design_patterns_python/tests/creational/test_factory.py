import unittest

from design_patterns.creational.factory import Factory


class FactoryTestCase(unittest.TestCase):
    def setUp(self):
        FactoryTestCase.logistics = Factory.createLogistics()

    def test_00_init_logistics(self):
        self.logistics = Factory.createLogistics()
        self.assertEqual(len(self.logistics), 0,
                         'Incorrect logistics size')

    def test_01_add_routes(self):
        FactoryTestCase.london_paris = Factory.createDeliveryRoute(
            'London', 'Paris')
        FactoryTestCase.bangkok_beijing = Factory.createDeliveryRoute(
            'Bangkok', 'Beijing')
        FactoryTestCase.berlin_rome = Factory.createDeliveryRoute(
            'Berlin', 'Rome')

        self.assertEqual(self.london_paris.fr, 'London',
                         'Incorrect from destination')
        self.assertEqual(self.bangkok_beijing.fr, 'Bangkok',
                         'Incorrect from destination')
        self.assertEqual(self.berlin_rome.fr, 'Berlin',
                         'Incorrect from destination')

        self.assertEqual(self.london_paris.to, 'Paris',
                         'Incorrect to destination')
        self.assertEqual(self.bangkok_beijing.to, 'Beijing',
                         'Incorrect to destination')
        self.assertEqual(self.berlin_rome.to, 'Rome',
                         'Incorrect to destination')

    def test_02_reverse_routes(self):
        FactoryTestCase.london_paris.reverse()

        self.assertEqual(self.london_paris.fr, 'Paris',
                         'Incorrect reversed from destination')

        FactoryTestCase.london_paris.reverse()

        self.assertEqual(self.london_paris.fr, 'London',
                         'Incorrect from destination')

    def test_03_add_transport(self):
        FactoryTestCase.truck1 = Factory.createTruck(self.london_paris)
        FactoryTestCase.truck2 = Factory.createTruck(self.berlin_rome)
        FactoryTestCase.train1 = Factory.createTrain(self.london_paris)
        FactoryTestCase.train2 = Factory.createTrain(self.berlin_rome)
        FactoryTestCase.ship1 = Factory.createShip(self.bangkok_beijing)

        self.assertEqual(self.truck1.name, 'Truck',
                         'Incorrect transport name')
        self.assertEqual(self.train1.name, 'Train',
                         'Incorrect transport name')
        self.assertEqual(self.ship1.name, 'Ship',
                         'Incorrect transport name')

    def test_04_add_logistics(self):
        self.logistics.add_transport(self.truck1)
        self.logistics.add_transport(self.truck2)
        self.logistics.add_transport(self.train1)
        self.logistics.add_transport(self.train2)
        self.logistics.add_transport(self.ship1)

        self.assertEqual(len(self.logistics), 5,
                         'Incorrect logistics size')

    def test_05_deliver_logistics(self):
        self.logistics.add_transport(self.truck1)
        self.logistics.add_transport(self.train1)
        self.logistics.add_transport(self.ship1)

        self.assertEqual(len(self.logistics), 3,
                         'Incorrect logistics size')

        self.logistics.deliver()
        self.assertEqual(len(self.logistics), 2,
                         'Incorrect logistics size')

        self.logistics.deliver()
        self.assertEqual(len(self.logistics), 1,
                         'Incorrect logistics size')

        self.logistics.deliver()
        self.assertEqual(len(self.logistics), 0,
                         'Incorrect logistics size')


if __name__ == '__main__':
    unittest.main()
