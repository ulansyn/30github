import matplotlib.pyplot as plt

# было скучно и я бросал игральную кость
rolls_str = "2162155214213453342565616141513363163113614466234513555364314565663212112533211214535316562145415464131212336215451636441416641125642236664335346"

total_counts = {str(i): 0 for i in range(1, 7)}
for roll in rolls_str:
    if roll in total_counts:
        total_counts[roll] += 1

print("Общий подсчет выпадений:")
for face in sorted(total_counts.keys()):
    print(f"Лицо {face}: {total_counts[face]} раз")

cumulative_counts = {str(i): [] for i in range(1, 7)}
current_counts = {str(i): 0 for i in range(1, 7)}
roll_numbers = []

for idx, roll in enumerate(rolls_str, start=1):
    if roll in current_counts:
        current_counts[roll] += 1
    for face in current_counts:
        cumulative_counts[face].append(current_counts[face] / idx)
    roll_numbers.append(idx)

plt.figure(figsize=(10, 6))
for face in sorted(cumulative_counts.keys()):
    plt.plot(roll_numbers, cumulative_counts[face],
             label=f'Сторона {face}', marker='o', markersize=2, linewidth=1)

plt.xlabel('Номер броска')
plt.ylabel('частота')
plt.title('Динамика')
plt.legend()
plt.grid(True)
plt.show()
