import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_excel('disaster_dataset.xlsx')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: File not found. Please check the file name and path.")
    exit()

# Data Preprocessing
if 'PassengerId' in df.columns:
    df = df.drop(['PassengerId'], axis=1)
# Fill missing Age with the median age
df['Age'] = df['Age'].fillna(df['Age'].median())
# Drop rows where 'Survived' or 'Sex' is missing
df = df.dropna(subset=['Survived', 'Sex'])

# Encode 'Sex' (Text -> Numbers)
le = LabelEncoder()
df['Sex'] = le.fit_transform(df['Sex'].astype(str))
X = df[['Pclass', 'Sex', 'Age', 'SibSp']] 
y = df['Survived']

# Train Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# Evaluate
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
# Predict survival for the ENTIRE dataset to see who the model thinks can be saved
all_predictions = model.predict(X)
df['Predicted_Survived'] = all_predictions
# Calculate Counts
total_people = len(df)
total_saved = df['Predicted_Survived'].sum()
print(f"Total People in Crowd: {total_people}")
print(f"Predicted to be Saved: {total_saved} ({total_saved/total_people*100:.1f}%)")

# Generate Graphs
plt.figure(figsize=(18, 5))
# Graph 1: Total People Saved vs Not Saved
plt.subplot(1, 3, 1)
ax1 = sns.countplot(x='Predicted_Survived', data=df, hue='Predicted_Survived', palette=['#FF9999', '#66B2FF'], legend=False)
plt.title('Total People Predicted to be Saved')
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
plt.ylabel('Ratio (0.0 = None, 1.0 = All)')
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