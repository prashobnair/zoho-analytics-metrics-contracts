# Zoho Analytics Metrics Contracts

An offline cross-app metrics contract for fictional CRM deals, Books invoices and People capacity. It joins records by an explicit account key, checks source freshness and refuses to mix currencies in a revenue total. Audience-specific output keeps finance and operations metrics out of the sales view. This is a JSON report, **not** a Zoho Analytics dashboard, a live connector or a claim of full user-level authorization.

## Contract use-case

A [Zoho Analytics/CRM dashboard brief](https://www.freelancer.com/projects/zoho-crm/zoho-analytics-crm-dashboard-creation) requests CRM, Books, People/Payroll joins, auto-refresh and permission-aware views. An older [CRM insights brief](https://www.freelancer.com/projects/zoho-crm/zoho-crm-insights-dashboard-setup) asks for customer behavior and purchase metrics. This repo demonstrates metric definitions, joins, freshness and a small view-boundary test, not the interactive visual or live refresh portion. These briefs are demand examples, not client work.

## Run

Python 3.10+ and standard library only. From the repo root:

```sh
python3 cli.py examples.json
python3 cli.py examples.json --audience operations
python3 cli.py examples.json --audience sales
python3 -m unittest discover -p 'test_*.py' -v
```

No Zoho trial, API key, Docker, web server or paid plan is required. The synthetic sample reports one won deal/account and USD 1200.00 paid net revenue in the finance view, 62.50% booked utilization in operations, plus stale Books snapshot and mismatched EUR invoice findings. Sales sees only won-deal/account counts. `dashboard: false` is intentional. See `DESIGN.md` for metric dictionary and the visual dashboard gap.

## Metric contract

`won_deals` counts CRM deals with stage `won` and a resolvable account; `won_accounts` counts distinct accounts with those deals. `paid_net_revenue` sums Books invoices with `status=paid`, valid account and the one declared currency, excluding mismatches. `booked_utilization_percent` is sum of booked hours / sum of available hours across all fictional staff, displayed to two decimals. A snapshot older than 24 hours is flagged as stale for this demo; that threshold is a design choice, not a vendor SLA. The fixture keys and stage names are fictional intermediate data, not official Zoho fields.

## Limits

A real dashboard needs agreed definitions, dimensional filters, row/field-level access, currency conversion rules, source refresh scheduling, query performance, visuals and export controls. Audience labels here are caller inputs, not authentication. Do not expose these reports to real users without authorization. No actual Zoho Analytics SQL/query, chart or scheduled PDF is supplied. `DESIGN.md` lists the acceptance path and missing tests.
