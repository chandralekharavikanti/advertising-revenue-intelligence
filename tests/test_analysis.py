import unittest
from src.generate_data import root
from src.analyze import analyze
class AnalysisTests(unittest.TestCase):
 def test_campaign_counts(self):
  result=analyze()
  self.assertEqual(result["kpis"]["campaign_count"],500)
  self.assertGreater(result["kpis"]["booked_revenue"],0)
if __name__=="__main__":unittest.main()
