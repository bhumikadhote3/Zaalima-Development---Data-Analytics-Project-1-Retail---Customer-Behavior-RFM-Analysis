import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Step 1: Create Demo Transaction Data
data = {
    'sales_key': [1,1,1,2,2,3,3,3,4,4],
    'product_name': [
        'Milk','Bread','Butter',
        'Rice','Dal',
        'Milk','Bread','Eggs',
        'Rice','Oil'
    ]
}

df_demo = pd.DataFrame(data)

# Step 2: Create Basket Matrix
basket = pd.crosstab(df_demo['sales_key'], df_demo['product_name'])

# Step 3: Convert to 0/1 (UPDATED FIX)
basket = (basket > 0)

frequent_items = apriori(basket, min_support=0.3, use_colnames=True)
rules = association_rules(frequent_items, metric="lift", min_threshold=1)

# Step 4: Apply Apriori
frequent_items = apriori(basket, min_support=0.3, use_colnames=True)

# Step 5: Generate Rules
rules = association_rules(frequent_items, metric="lift", min_threshold=1)

print("Frequent Itemsets:")
print(frequent_items)

print("\nAssociation Rules:")
print(rules[['antecedents','consequents','support','confidence','lift']])