# unittest file for calculator.

import unittest

from calculator import Calculator

class CalculatorTest(unittest.TestCase):
    def test_price_jump(self):
        """
        The average of current spot_price is out 3 sigma range and original data is also out.
        Expect: Consider price jump, use avg(spot price) directly
        Spot price: [50000, 50001, 50002]
        Past index price in last 5 minutes: [49200, 49800,49900,49000, 48000]
        Latest sigma: 150
        """
        c = Calculator()
        c.test_mode = True
        c.spot_prices = [50000, 50001, 50002]
        c.last_sigma = 150
        c.last_mean = 49000
        c.past_price = [49200, 49800, 49900, 49000, 48000]
        result = c.calculate()
        self.assertEqual(result[0], 50001)
        self.assertEqual(result[1], 693.9861710117541 )
        self.assertEqual(result[2], 49316.833333333336)

    def test_price_in_range(self):
        """
        The average of current spot_price is in 3 sigma range.
        Expect: Normal case, use avg(spot price) directly
        Spot price: [50000, 50001, 50002]
        Past index price in last 5 minutes: [49200, 49800,49900,49000, 48000]
        Latest sigma: 150
        """
        c = Calculator()
        c.test_mode = True
        c.spot_prices = [49300, 49200, 49100]
        c.last_sigma = 150
        c.last_mean = 49000
        c.past_price = [49200, 49800, 49900, 49000, 48000]
        result = c.calculate()
        self.assertEqual(result[0], 49200)
        self.assertEqual(result[1], 622.9410530343586 )
        self.assertEqual(result[2], 49183.333333333336)


    def test_minor_current_price_out_range(self):
        """
        1. The average of current spot_price is out of 3 sigma range.
        2. two of three price is in 3 sigma range, meaning one data is invalid
        Expect: only use the two price to calculate index.
        Spot price: [40000, 50001, 50002]
        Past index price in last 5 minutes: [49200, 49800,49900,49000, 48000]
        Latest sigma: 150
        """
        c = Calculator()
        c.test_mode = True
        c.spot_prices = [49100, 49200, 51100]
        c.last_sigma = 150
        c.last_mean = 49000
        c.past_price = [49200, 49800, 49900, 49000, 48000]
        result = c.calculate()
        self.assertEqual(result[0], 49150)
        self.assertEqual(result[1], 622.9967897188557)
        self.assertEqual(result[2], 49175.0)



if __name__ == '__main__':
    unittest.main()