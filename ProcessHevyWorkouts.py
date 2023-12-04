# Databricks notebook source
# Add imports, read in data to analyze
import json
import matplotlib.pyplot as plt
from pyspark.sql.functions import rand, sum, desc, isnull, col, avg, count, when, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark.conf.set(
    "fs.azure.account.key.athleteperformstore.dfs.core.windows.net",
    dbutils.secrets.get(scope="AthletePerformScope", key="MySecretKey"))

uri = "abfss://f23-proj@athleteperformstore.dfs.core.windows.net/"

# Hevy
hevy_workouts_df = spark.read.csv(uri + '/HevyWorkouts.csv', header=True)

# COMMAND ----------

# MAGIC %md
# MAGIC # Display Hevy data
# MAGIC One row = one workout
# MAGIC
# MAGIC 2 most important metrics:
# MAGIC - duration (how long training session)
# MAGIC - estimated_volume_kg (how much total weight lifted)

# COMMAND ----------

display(hevy_workouts_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC Show volume lifted. Compare workouts

# COMMAND ----------

#workout_rows = hevy_workouts_df.take(2)

# compare two random workouts
workout_rows = hevy_workouts_df.orderBy(rand()).take(2)

# Convert start and end times from strings to integers and calculate duration in minutes
workout1_duration_minutes = (int(workout_rows[0]['end_time']) - int(workout_rows[0]['start_time'])) / 60
workout2_duration_minutes = (int(workout_rows[1]['end_time']) - int(workout_rows[1]['start_time'])) / 60

workout1_volume = float(workout_rows[0]['estimated_volume_kg'])
workout2_volume = float(workout_rows[1]['estimated_volume_kg'])

# display these values in a 2x2 grid using matplotlib
workouts = ['Workout 1', 'Workout 2']
durations = [workout1_duration_minutes, workout2_duration_minutes]
volumes = [workout1_volume, workout2_volume]  # Make sure these are numeric
x = range(len(workouts))  # x-coordinates for the bars

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Ensure we only provide two colors for the two bars
colors = ['blue', 'green']

# Plotting Duration of Each Workout
axs[0, 0].bar(x, durations, color=colors)
axs[0, 0].set_xticks(x)
axs[0, 0].set_xticklabels(workouts)
axs[0, 0].set_title('Duration of Each Workout (in minutes)')
axs[0, 0].set_ylabel('Duration (minutes)')

# Plotting Total Volume for Each Workout
axs[1, 0].bar(x, volumes, color=colors)
axs[1, 0].set_xticks(x)
axs[1, 0].set_xticklabels(workouts)
axs[1, 0].set_title('Total Volume of Each Workout (in kg)')
axs[1, 0].set_ylabel('Volume (kg)')

# Setting the other plots as empty/blank
axs[0, 1].axis('off')
axs[1, 1].axis('off')

# Add labels on top of the bars with center alignment
for i, v in enumerate(durations):
    axs[0, 0].text(i, v, f'{round(v)}', ha='center', va='bottom', fontweight='bold')
for i, v in enumerate(volumes):
    # Make sure to add a small offset to 'v' to position the label above the bar
    axs[1, 0].text(i, v, f'{round(v)}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

# COMMAND ----------


