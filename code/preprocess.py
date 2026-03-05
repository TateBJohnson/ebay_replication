import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Path("temp").mkdir(parents=True, exist_ok=True)

# -------------------------
# Step 1 — Load and prepare data
# -------------------------

df = pd.read_csv('input/PaidSearch.csv')
df['date'] = pd.to_datetime(df['date'])
df['log_revenue'] = np.log(df['revenue'])

# -------------------------
# Step 2 — Separate treated and untreated units
# -------------------------

treated = df[df['search_stays_on'] == 0]
untreated = df[df['search_stays_on'] == 1]

treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

treated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']
untreated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']

treated_pivot['log_revenue_diff'] = (
    treated_pivot['log_revenue_post'] - treated_pivot['log_revenue_pre']
)

untreated_pivot['log_revenue_diff'] = (
    untreated_pivot['log_revenue_post'] - untreated_pivot['log_revenue_pre']
)

treated_pivot.to_csv('temp/treated_pivot.csv')
untreated_pivot.to_csv('temp/untreated_pivot.csv')

# -------------------------
# Step 3 — Print summary statistics
# -------------------------

print("Treated DMAs:", treated['dma'].nunique())
print("Untreated DMAs:", untreated['dma'].nunique())
print("Date range:", df['date'].min().date(), "to", df['date'].max().date())

# -------------------------
# Step 4 — Reproduce Figure 5.2
# -------------------------

avg_rev = df.groupby(['date', 'search_stays_on'])['revenue'].mean().reset_index()

control = avg_rev[avg_rev['search_stays_on'] == 1]
treatment = avg_rev[avg_rev['search_stays_on'] == 0]

plt.figure()
plt.plot(control['date'], control['revenue'], label='Control (search stays on)')
plt.plot(treatment['date'], treatment['revenue'], label='Treatment (search goes off)')
plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Average Revenue Over Time')
plt.legend()
plt.tight_layout()
plt.savefig('output/figures/figure_5_2.png')
plt.close()

# -------------------------
# Step 5 — Reproduce Figure 5.3
# -------------------------

avg_log = df.groupby(['date', 'search_stays_on'])['log_revenue'].mean().reset_index()

pivot_log = avg_log.pivot(
    index='date',
    columns='search_stays_on',
    values='log_revenue'
)

pivot_log['difference'] = pivot_log[1] - pivot_log[0]

plt.figure()
plt.plot(pivot_log.index, pivot_log['difference'])
plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')
plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Log Revenue Difference Over Time')
plt.tight_layout()
plt.savefig('output/figures/figure_5_3.png')
plt.close()

