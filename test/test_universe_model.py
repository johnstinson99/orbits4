import unittest
from src.universe_model import UniverseModel
from src.celestial_body import Body


class TestBarycentreFormula(unittest.TestCase):

    body1 = Body(mass=1, x=10)
    body2 = Body(mass=2, x=100)
    body3 = Body(mass=3, x=50)
    # body1 and body2 should have a barycentre of 70
    # adding in body3 should give a barycentre of 60

    universe_model = UniverseModel()

    def test_barycentre_2_bodies(self):
        my_body_list = [TestBarycentreFormula.body1, TestBarycentreFormula.body2]
        TestBarycentreFormula.universe_model.body_list = my_body_list
        barycentre = TestBarycentreFormula.universe_model.get_barycentre()
        # centre of 1 and 2 =  (m0*x0 + m1*x1 ) / (m0 + m1)
        # = 10 + 200 / (1 + 2)
        # = 210/3
        # = 70 (3)
        self.assertEqual(barycentre, 70)

    def test_barycentre_3_bodies(self):
        my_body_list = [TestBarycentreFormula.body1, TestBarycentreFormula.body2, TestBarycentreFormula.body3]
        TestBarycentreFormula.universe_model.body_list = my_body_list
        barycentre = TestBarycentreFormula.universe_model.get_barycentre()
        # print("barycentre is", barycentre, " should be 60")
        # x = (m0*x0 + m1*x1 + m2*x2 ) / (m0 + m1 + m2)
        # = 10 + 200 +150/ (1 + 2 + 3)
        # = 360/6
        # = 60 - correct
        self.assertEqual(barycentre, 60)


# if __name__ == '__main__':
#     unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(TestBarycentreFormula)
unittest.TextTestRunner(verbosity=2).run(suite)

