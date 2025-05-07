import unittest

from design_patterns.creational.builder import (Engine, Fuel, Transmission,
                                                VehicleBlueprint,
                                                VehicleBuilder, VehicleBuilt)


class BuilderTestCase(unittest.TestCase):

    def test_00_init_builder(self):
        BuilderTestCase.builder_ford_f_100 = VehicleBuilder(
            VehicleBlueprint(
                engine=Engine(Fuel.diesel, 6),
                transmission=Transmission.manual,
                wheels=4,
                seats=6
            )
        )

        BuilderTestCase.builder_tesla_model_3 = VehicleBuilder(
            VehicleBlueprint(
                engine=Engine(Fuel.gasoline, 4),
                transmission=Transmission.automatic,
                wheels=2,
                seats=2
            )
        )

        BuilderTestCase.builder_kawasaki_ninja_1000 = VehicleBuilder(
            VehicleBlueprint(
                engine=Engine(Fuel.electric),
                transmission=Transmission.automatic,
                wheels=4,
                seats=6
            )
        )

    def test_01_test_bad_config(self):
        with self.assertRaises(Exception):
            VehicleBlueprint(
                engine=Engine(engine=Fuel.electric, cylinders=1),
                transmission=Transmission.automatic,
                wheels=4,
                seats=6
            )
        with self.assertRaises(Exception):
            VehicleBlueprint(
                engine=Engine(engine=Fuel.diesel, cylinders=0),
                transmission=Transmission.automatic,
                wheels=4,
                seats=6
            )

    def test_02_test_builder_incomplete(self):

        self.builder_ford_f_100.build_engine()
        self.builder_ford_f_100.build_transmission()
        self.builder_ford_f_100.build_wheels()

        exported_ford = self.builder_ford_f_100.export()
        self.assertIsNone(exported_ford)
        self.assertIsNotNone(self.builder_ford_f_100.vehicle.engine)
        self.assertIsNotNone(self.builder_ford_f_100.vehicle.transmission)
        self.assertIsNotNone(self.builder_ford_f_100.vehicle.wheels)
        self.assertIsNone(self.builder_ford_f_100.vehicle.seats)

    def test_03_test_builder_complete(self):

        self.builder_ford_f_100.build_seats()
        exported_ford = self.builder_ford_f_100.export()

        self.assertIsNotNone(exported_ford)
        self.assertIsInstance(exported_ford, VehicleBuilt)


if __name__ == '__main__':
    unittest.main()
