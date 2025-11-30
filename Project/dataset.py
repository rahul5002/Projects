import pandas as pd
import numpy as np

NUM_ROWS = 10000
np.random.seed(42) 
# To generate features
# Pclass: More people in class 3 than class 1
pclass = np.random.choice([1, 2, 3], size=NUM_ROWS, p=[0.2, 0.3, 0.5])
# Sex: Roughly 50/50 split
sex = np.random.choice(['male', 'female'], size=NUM_ROWS)
# Random ages between 1 and 80
age = np.random.randint(1, 80, size=NUM_ROWS)
# SibSp: Most people travel alone (0) or with 1 person
sibsp = np.random.choice([0, 1, 2, 3, 4, 5, 8], size=NUM_ROWS, p=[0.6, 0.25, 0.1, 0.02, 0.01, 0.01, 0.01])
# Survival logic
# Start with a base survival probability of 20%
survival_prob = np.full(NUM_ROWS, 0.2)
# Adjust probability based on demographics (The "Women and Children First" rule)
# If Female, add 50% survival chance
survival_prob = np.where(sex == 'female', survival_prob + 0.50, survival_prob)
# If Class 1 (Rich), add 20% survival chance
survival_prob = np.where(pclass == 1, survival_prob + 0.20, survival_prob)
# If Child (Under 10), add 30% survival chance
survival_prob = np.where(age < 10, survival_prob + 0.30, survival_prob)
# Cap probabilities at 0 and 1
survival_prob = np.clip(survival_prob, 0, 1)
# Generate final 0 or 1 outcome based on the probability
survived = np.random.binomial(1, survival_prob)

df = pd.DataFrame({
    'PassengerId': range(1, NUM_ROWS + 1),
    'Pclass': pclass,
    'Sex': sex,
    'Age': age,
    'SibSp': sibsp,
    'Survived': survived
})

try:
    df.to_excel('disaster_dataset.xlsx', index=False)
    print(f"Success! Generated {NUM_ROWS} rows in 'large_disaster_dataset.xlsx'")
    print(df.head())
except ImportError:
    print("Error: You need openpyxl installed. Run: pip install openpyxl")