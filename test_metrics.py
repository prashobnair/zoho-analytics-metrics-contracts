import copy
import json
import unittest
from pathlib import Path
from metrics import evaluate

DATA = json.loads(Path(__file__).with_name('examples.json').read_text())

class MetricsTests(unittest.TestCase):
    def test_finance_metrics_with_findings(self):
        r = evaluate(DATA)
        self.assertEqual('1200.00', r['metrics']['paid_net_revenue'])
        self.assertEqual(1, r['metrics']['won_deals'])
        self.assertEqual({'stale_snapshot','currency_mismatch'}, {x['code'] for x in r['findings']})
        self.assertFalse(r['dashboard'])

    def test_operations_audience(self):
        r = evaluate(DATA, 'operations')
        self.assertEqual('62.50', r['metrics']['booked_utilization_percent'])
        self.assertNotIn('paid_net_revenue', r['metrics'])

    def test_sales_audience(self):
        r = evaluate(DATA, 'sales')
        self.assertEqual({'won_deals':1,'won_accounts':1}, r['metrics'])

    def test_orphan_deal(self):
        data = copy.deepcopy(DATA)
        data['deals'][0]['account_id'] = 'missing'
        self.assertIn('orphan_deal', [x['code'] for x in evaluate(data)['findings']])

    def test_naive_timestamp(self):
        data = copy.deepcopy(DATA)
        data['as_of'] = '2026-09-26T12:00:00'
        with self.assertRaises(ValueError):
            evaluate(data)

    def test_invalid_utilization(self):
        data = copy.deepcopy(DATA)
        data['staff'][0]['hours_booked'] = 80
        self.assertIn('invalid_utilization', [x['code'] for x in evaluate(data, 'operations')['findings']])

if __name__ == '__main__':
    unittest.main()
