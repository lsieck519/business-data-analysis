## Example Stakeholder Message

**Requirements:**
* Highlight key data quality issues.
* Include one interesting trend observed in the data.
* Provide a clear request for action.
---
**Example Message:** 

Subject: Key Data Quality Insights & Action Items

Hi ___,

I’ve identified several data quality issues that could impact our business insights and decision-making:

- **User Data:** Key fields such as `BIRTH_DATE`, `STATE`, `LANGUAGE`, and `GENDER` contain missing values. Additionally, the `GENDER` field has inconsistencies in how options are recorded (e.g., "Prefer not to say" vs. "prefer_not_to_say").  
- **Transaction Data:** Some `FINAL_QUANTITY` values are appearing as "zero" instead of numerical values, and there are discrepancies in `STORE_NAME` formatting (e.g., "PRICE CUTTER" vs. "PRICE UTTER").  
- **Product Data:** Missing product categories and placeholder values for `MANUFACTURER` and `BRAND` could affect reporting accuracy.  

**Key Trend to Highlight:**  
User growth has declined significantly, with a **-42.31% drop** from 2022 to 2023, followed by another **-24.79% decrease** in 2024. This trend may require further investigation to understand potential business impacts.

I've created a [Tableau dashboard](https://public.tableau.com/views/BusinessDataSummary/UserGrowth?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) to visualize these trends and suggest reviewing it during our upcoming biweekly sync next Tuesday.

**Recommended Actions:**  
1. Standardize data entry for fields such as `GENDER` and `STORE_NAME` to improve consistency and reliability.  
2. Address missing values in user and transaction data where possible to ensure completeness in reporting.  

I will create tickets with additional details. Please let me know who the best point of contact would be to discuss standardizing user fields on the registration page.

Let me know if you have any questions or if you'd like to dive deeper into any of these points.

Thanks,  
Laura
