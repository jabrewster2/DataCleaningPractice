# DataCleaningPractice
Claude made a messy data set about orders and I had to clean it using pandas so that the data was separated into a standard format and the data that could not be parsed was separated into its own file. 
## Rules by Column

| Column | Standard | How to handle problems |
|---|---|---|
| `order_id` | Uppercase, trimmed, format `ORD-####` | Trim whitespace. IDs must be unique after cleaning. |
| `customer_name` | Trimmed, Title Case, from an approved list: Carl, Princess Donut, Mordecai | Map variants with a lookup table (`carl` → Carl, `Donut` → Princess Donut). Blank or `N/A` becomes null and gets flagged. Keep the row, since the order still happened. |
| `order_date` | ISO 8601, `YYYY-MM-DD` | Read slash dates as US `MM/DD/YYYY`. Valid range is 2026-01-01 to today. Impossible, future, or pre-2026 dates become null and get flagged. Don't guess. |
| `city` | Trimmed, Title Case | `MOBILE`, `mobile`, and ` Mobile ` all become `Mobile`. |
| `item` | Trimmed, must exactly match the 12-item catalog (see below) | Normalize case and whitespace, then match. Unknown or blank items go to quarantine. |
| `quantity` | Whole number from 1 to 100 | Negative, 0, and 9999 are invalid and become null. Recover as `order_amount ÷ unit_price` if both are valid and flag `qty_recovered`. Otherwise quarantine. Text such as `"two"` converts to 2 and is flagged. |
| `unit_price` | Numeric, 2 decimals, no symbols | Strip `$`, commas, and `USD`. Negative, blank, or mismatched prices are replaced with the catalog price and flagged `price_corrected`. |
| `order_amount` | Numeric, 2 decimals, equal to quantity × unit price | Recalculate if missing. Flag mismatches. |
| `status` | Title Case from a fixed list: Pending, Shipped, Delivered, Cancelled | Fix typos (`shiped` → Shipped). Blank becomes `Unknown`. |
| `notes` | Trimmed free text | Blank is fine. |

### Item Catalog

| Item | Catalog Price |
|---|---|
| Healing Potion | 45.00 |
| Iron Dagger | 320.50 |
| Leather Boots | 180.00 |
| Cat Treats (Bulk) | 24.99 |
| Sparkly Tiara | 1250.00 |
| Ration Crate | 75.25 |
| Torch Bundle | 12.50 |
| Climbing Rope | 58.00 |
| Grooming Kit | 96.75 |
| Padded Armor Set | 1480.00 |
| Lockpick Set | 210.00 |
| Map Scroll | 33.00 |

Assumption: prices never changed over time, so the catalog price applies to every order.
