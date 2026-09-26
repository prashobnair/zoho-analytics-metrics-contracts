# Metric dictionary and review

| Metric | Formula | Source | Audience in this demo | Limitation |
| --- | --- | --- | --- | --- |
| won_deals | Count won deals with an account | fictional CRM | sales, finance, operations | Stage semantics not verified |
| won_accounts | Distinct account IDs among won deals | fictional CRM | sales, finance, operations | No identity resolution |
| paid_net_revenue | Sum paid invoice net amounts in declared currency | fictional Books | finance | No FX, credits, tax or period filter |
| booked_utilization_percent | 100 × booked / available hours | fictional People | operations | Aggregate only, no employee details |

## Join and freshness policy

The fixture's explicit account IDs are the join key; names are not used. Orphan deals/invoices are findings. A mismatched invoice currency is excluded from the sum and flagged, never converted by a guessed rate. All timestamps require offsets; a source snapshot older than 24 hours is flagged. A future snapshot is also flagged. In a real app, each source may have different update cadence and effective time; an agreed service-level definition must replace the demo threshold.

## Permissions and dashboard gap

`--audience` is a test selector, not an authenticated user. The finance total is omitted from sales and operations output; operations utilization is omitted from sales and finance. Findings may still reveal source identifiers and must also be access-controlled in production. A real Zoho Analytics build would require current connector/API metadata, row-level policy, live refresh, validated query plans, interactive chart design, scheduled exports and pixel inspection. None is claimed by this JSON prototype.

## Acceptance and tests

Six tests cover finance/operations/sales output, orphan join, naive time rejection and invalid utilization. Review expected values with finance, sales and operations owners using fictional fixtures, then test role isolation and refresh in a sandbox. Add duplicate ID detection, period windows, timezone/reporting currency, partial payments, credit notes, payroll sensitivity, performance and visual verification before a live deployment.
