import matplotlib.pyplot as plt

# Data
labels = ['Male', 'Female']
sizes = [68, 37]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)  # explode 1st slice

# Patient demographics
average_age_male = 66.4
average_age_female = 69.6
age_range_male = "31-88"
age_range_female = "46-93"

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                  autopct='%1.1f%%', startangle=140)
plt.setp(autotexts, size=10, weight="bold")
ax.set_title('Distribution of Male and Female Patients')

# Annotate with average ages and age ranges
ax.text(-1.3, 1, f'Average Age (Male): {average_age_male} years\nAge Range (Male): {age_range_male} years', fontsize=10)
ax.text(-1.3, 0.8, f'Average Age (Female): {average_age_female} years\nAge Range (Female): {age_range_female} years', fontsize=10)

plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
