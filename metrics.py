"""Offline metrics contracts across fictional CRM, Books and People tables."""
from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation


def instant(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (AttributeError, ValueError) as exc:
        raise ValueError('Invalid timestamp') from exc
    if dt.tzinfo is None:
        raise ValueError('Timestamp requires timezone')
    return dt.astimezone(timezone.utc)


def evaluate(data, audience='finance'):
    if not isinstance(data, dict) or audience not in {'sales', 'finance', 'operations'}:
        raise ValueError('Expected data and audience sales/finance/operations')
    for key in ('accounts', 'deals', 'invoices', 'staff'):
        if not isinstance(data.get(key), list):
            raise ValueError(f'{key} must be list')
    as_of = instant(data.get('as_of'))
    accounts = {}
    for row in data['accounts']:
        key = row.get('id')
        if not key or key in accounts:
            raise ValueError('Account IDs must be unique')
        accounts[key] = row
    findings = []
    for name in ('crm', 'books', 'people'):
        updated = instant(data.get('updated_at', {}).get(name))
        if updated > as_of:
            findings.append({'code':'future_snapshot','source':name})
        elif (as_of - updated).total_seconds() > 86400:
            findings.append({'code':'stale_snapshot','source':name})
    deal_count = 0
    won_accounts = set()
    for deal in data['deals']:
        account = deal.get('account_id')
        if account not in accounts:
            findings.append({'code':'orphan_deal','source':str(deal.get('id',''))})
            continue
        if deal.get('stage') == 'won':
            deal_count += 1
            won_accounts.add(account)
    revenue = Decimal('0')
    for invoice in data['invoices']:
        if invoice.get('account_id') not in accounts:
            findings.append({'code':'orphan_invoice','source':str(invoice.get('id',''))})
            continue
        try:
            value = Decimal(str(invoice['net_amount']))
        except (KeyError, InvalidOperation) as exc:
            raise ValueError('Invalid invoice amount') from exc
        if not value.is_finite() or value < 0:
            raise ValueError('Invalid invoice amount')
        if invoice.get('currency') != data.get('currency'):
            findings.append({'code':'currency_mismatch','source':str(invoice.get('id',''))})
            continue
        if invoice.get('status') == 'paid':
            revenue += value
    utilization = None
    if data['staff']:
        total = sum(Decimal(str(x.get('hours_available', 0))) for x in data['staff'])
        used = sum(Decimal(str(x.get('hours_booked', 0))) for x in data['staff'])
        if total <= 0 or used < 0 or used > total:
            findings.append({'code':'invalid_utilization','source':'people'})
        else:
            utilization = str((used / total * 100).quantize(Decimal('0.01')))
    metrics = {'won_deals':deal_count,'won_accounts':len(won_accounts)}
    if audience == 'finance':
        metrics['paid_net_revenue'] = str(revenue)
        metrics['currency'] = data.get('currency')
    if audience == 'operations':
        metrics['booked_utilization_percent'] = utilization
    return {'audience':audience,'metrics':metrics,'findings':findings,'as_of':as_of.isoformat(),
            'dashboard':False}
