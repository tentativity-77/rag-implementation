 python query.py
Received notification from DBMS server: <GqlStatusObject gql_status='01N01', status_description='warn: feature deprecated with replacement. db.index.vector.queryNodes is deprecated. It is replaced by SEARCH.', position=<SummaryInputPosition line=1, column=1, offset=0>, raw_classification='DEPRECATION', classification=<NotificationClassification.DEPRECATION: 'DEPRECATION'>, raw_severity='WARNING', severity=<NotificationSeverity.WARNING: 'WARNING'>, diagnostic_record={'_classification': 'DEPRECATION', '_severity': 'WARNING', '_position': {'offset': 0, 'line': 1, 'column': 1}, 'OPERATION': '', 'OPERATION_CODE': '0', 'CURRENT_SCHEMA': '/'}> for query: "CALL db.index.vector.queryNodes($vector_index_name, $top_k * $effective_search_ratio, $query_vector) YIELD node, score WITH node, score LIMIT $top_k RETURN reduce(str='', k IN ['text'] | str + '\\n' + k + ': ' + coalesce(node[k], '')) AS text, node {.*, `embedding`: Null, `text`: Null} AS metadata, score"
METADATA KEYS: {'moddate': '2026-07-10T09:13:13+00:00', 'creator': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', 'creationdate': '2026-07-10T09:13:13+00:00', 'producer': 'Skia/PDF m149', 'id': '2efc6d1f1b15df3b0f8f526f0b34430f', 'source': 'data/nintendo.pdf', 'total_pages': 4, 'page': 0, 'title': 'Nintendo Store Refunds & Returns', 'page_label': '1'}
METADATA KEYS: {'moddate': '2026-07-10T09:13:13+00:00', 'creator': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', 'creationdate': '2026-07-10T09:13:13+00:00', 'producer': 'Skia/PDF m149', 'id': '181f4d0333653cdd0c749a57fd6ee799', 'source': 'data/nintendo.pdf', 'total_pages': 4, 'page': 1, 'title': 'Nintendo Store Refunds & Returns', 'page_label': '2'}
METADATA KEYS: {'moddate': '2026-07-10T09:13:13+00:00', 'creator': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', 'creationdate': '2026-07-10T09:13:13+00:00', 'producer': 'Skia/PDF m149', 'id': '3e9c2fcbd34b62bd9050214591f18b71', 'source': 'data/nintendo.pdf', 'total_pages': 4, 'page': 0, 'title': 'Nintendo Store Refunds & Returns', 'page_label': '1'}
=====context_used=====Relevant text excerpts:

text: Nintendo Store physical product return policy
You have 30 days after delivery of your order to return or exchange products purchased
directly from the . Nintendo will not refund the cost of shipping unless the
return is a result of Nintendo providing a product that is damaged, defective, or different
than the product you ordered.
Nintendo will not accept returns or exchanges for the following items:
1. Any items that are shipped to Nintendo after 30 days from delivery.
2. Any items that have been opened, unsealed, or had tags removed.
3. Any item that is not in its original condition, is damaged, shows signs of use or is
missing parts.
4. Any items that were not purchased directly from the Nintendo Store.
5. Any digital item including digital games, download content (DLC), subscriptions, and
download codes (including any physical products that include digital items, such as
Nintendo eShop cards). 
Requesting a Return or Exchange
To return an item for a refund or exchange, please send the item in its original packaging,
with all parts to the appropriate address listed below, along with an explanation of the
issue and whether you are requesting a refund or exchange. Be sure to include your name,
address, daytime phone number, email address, and your original order number. Please
send the package via a registered or insured shipping method as Nintendo will not be
responsible for lost or misdirected packages.
U.S. Residents:
Nintendo of America Inc.
Attn: CS Returns
---

text: Nintendo of Canada Ltd.
Attn: CS Returns
Unit 120
2935 Hebb Avenue
Vancouver, BC
V5M 4Y2
Credits for properly returned items will be applied to the payment method that was used
for the order. If credit card payment was used, the credit will be applied to the same
credit card number that was used for the original order. Credits should appear within two
billing cycles. Nintendo reserves the right to limit or decline refunds or exchanges.
If you need further assistance with your return or exchange, please  .  
Other policies:
contact us
Digital products refund policy
Nintendo NEW YORK and Nintendo SAN FRANCISCO return policy
About Nintendo
Careers
Corporate Social Responsibility
Shop
Games
Hardware
Merchandise
Sales and deals
Exclusives
Nintendo Switch Online
Nintendo retail locations
Orders SupportSkip to main content
10/07/2026, 17:13 Nintendo Store Refunds & Returns
https://www.nintendo.com/us/refund-return-policy/nintendo-store/ 2/4
---

text: send the package via a registered or insured shipping method as Nintendo will not be
responsible for lost or misdirected packages.
U.S. Residents:
Nintendo of America Inc.
Attn: CS Returns
5001 150th Ave NE
Redmond, WA 98052
Canadian Residents:
Nintendo Store
Skip to main content
10/07/2026, 17:13 Nintendo Store Refunds & Returns
https://www.nintendo.com/us/refund-return-policy/nintendo-store/ 1/4
## Nintendo Store Return Policy

Based on the Nintendo Store return policy, **you would not be eligible for a return or exchange** if your item was purchased last year.

The policy clearly states:

> *"You have **30 days after delivery** of your order to return or exchange products purchased directly from the Nintendo Store."*

Additionally, Nintendo explicitly will **not accept returns or exchanges** for:

> *"Any items that are shipped to Nintendo **after 30 days from delivery**."*

Since a purchase made last year would be well beyond the **30-day return window**, Nintendo would not accept a return or exchange for that item.