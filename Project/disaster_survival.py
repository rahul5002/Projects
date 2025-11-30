import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

try:
    df = pd.read_excel('disaster_dataset.xlsx')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: File not found. Please check the file name and path.")
    exit()

# Data Preprocessing
if 'PassengerId' in df.columns:
    df = df.drop(['PassengerId'], axis=1)

# Fill missing Age
df['Age'] = df['Age'].fillna(df['Age'].median())
# Drop rows with missing critical info
df = df.dropna(subset=['Survived', 'Sex'])
# Encode 'Sex'
le = LabelEncoder()
df['Sex'] = le.fit_transform(df['Sex'].astype(str))

X = df[['Pclass', 'Sex', 'Age', 'SibSp']] 
y = df['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Comparison Loop
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}
results = {}
best_model = None
best_model_name = ""
best_acc = 0.0
print("\n--- Model Competition Results ---")
for name, model in models.items():
    # Train
    model.fit(X_train, y_train)
    # Predict
    y_pred = model.predict(X_test)
    # Evaluate
    acc = accuracy_score(y_test, y_pred)
    results[name] = acc
    print(f"{name}: {acc*100:.2f}%")

    if acc > best_acc:
        best_acc = acc
        best_model = model
        best_model_name = name
print(f"\nWINNER: **{best_model_name}** with {best_acc*100:.2f}% accuracy.")
print(f"Proceeding to Crowd Analysis using {best_model_name}...\n")

# Comparison Graph to show which model won
plt.figure(figsize=(8, 5))
results_df = pd.DataFrame(list(results.items()), columns=['Model', 'Accuracy'])
ax_comp = sns.barplot(x='Model', y='Accuracy', data=results_df, hue='Model', palette='viridis', legend=False)
plt.title('Model Accuracy Comparison')
plt.ylim(0, 1.1)
for p in ax_comp.patches:
    ax_comp.annotate(f'{p.get_height()*100:.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='center', xytext=(0, 10), textcoords='offset points')
plt.show()

# Crowd Analysis (Using the Best Model) 
# Predicting survival for the ENTIRE dataset using the winner
all_predictions = best_model.predict(X)
df['Predicted_Survived'] = all_predictions
# Calculate Counts
total_people = len(df)
total_saved = df['Predicted_Survived'].sum()
print(f"Total People in Crowd: {total_people}")
print(f"Predicted to be Saved: {total_saved} ({total_saved/total_people*100:.1f}%)")

plt.figure(figsize=(18, 5))
# Graph 1: Total People Saved vs Not Saved
plt.subplot(1, 3, 1)
ax1 = sns.countplot(x='Predicted_Survived', data=df, hue='Predicted_Survived', palette=['#FF9999', '#66B2FF'], legend=False)
plt.title(f'Total People Saved (Model: {best_model_name})')
plt.xticks([0, 1], ['Not Saved', 'Saved'])
plt.ylabel('Count')
for p in ax1.patches:
    if p.get_height() > 0: 
        ax1.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='center', xytext=(0, 10), textcoords='offset points')

# Graph 2: Ratio Saved by Gender
df['Sex_Label'] = df['Sex'].apply(lambda x: 'Male' if x == 1 else 'Female')
plt.subplot(1, 3, 2)
ax2 = sns.barplot(x='Sex_Label', y='Predicted_Survived', data=df, hue='Sex_Label', palette='coolwarm', errorbar=None, legend=False)
plt.title('Survival Ratio by Gender')
plt.ylabel('Ratio (0.0 - 1.0)')
plt.ylim(0, 1)
for p in ax2.patches:
    if p.get_height() > 0:
        ax2.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='center', xytext=(0, 10), textcoords='offset points')

# Graph 3: Ratio Saved by Age Group
bins = [0, 12, 18, 60, 100]
labels = ['Child (0-12)', 'Teen (12-18)', 'Adult (18-60)', 'Elderly (60+)']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)
plt.subplot(1, 3, 3)
ax3 = sns.barplot(x='AgeGroup', y='Predicted_Survived', data=df, hue='AgeGroup', palette='viridis', errorbar=None, legend=False)
plt.title('Survival Ratio by Age Group')
plt.ylabel('Ratio Saved')
plt.ylim(0, 1)

plt.tight_layout()
plt.show()
