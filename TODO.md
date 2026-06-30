Create `INVOICE_LINE_ITEMS` table.
Instead of contract to invoice, make it contract to invoice line items then to invoice.
Can edit line items (like price per unit and number of units).
Can add new line items such as Telkomsel charges, Performance Assurance, flight ticket reimbursements, etc.

Create `AGGREGATE_UNINSTALLED` table.

Add `due_date` to `RECEIVABLES` and `REVENUES`.
Past due?

When generating invoices, auto-generate the invoice number. Also auto-generate due date to H+14.

MRR & ARR by Resource, by Site Legal Name, by Customer Legal Name