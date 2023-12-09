from PIL import Image
import matplotlib.pyplot as plt
from num2words import num2words
from collections import Counter
from tqdm import tqdm

def count_letters_in_numbers(max_num):
    number_letter_map = []
    for num in range(1, max_num + 1):
        word = num2words(num).replace(" ", "").replace("-", "").lower()
        number_letter_map.append(Counter(word))
    return number_letter_map

max_number = 1000
number_letter_map = count_letters_in_numbers(max_number)

fig, ax = plt.subplots()
cumulative_counts = Counter()

def update_plot(frame):
    cumulative_counts.update(number_letter_map[frame])
    ax.clear()
    ax.set_title(f"Cumulative Letter Frequency in Numbers (1 to {frame + 1})")
    ax.bar(cumulative_counts.keys(), cumulative_counts.values())
    ax.set_xlabel("Letters")
    ax.set_ylabel("Cumulative Frequency")

# Generate and save selected frames based on order of magnitude
frame_images = []
for frame in tqdm(range(max_number), desc="Creating Selected Frames"):
    update_plot(frame)
    order_of_magnitude = len(str(frame))

    # Determine frame saving frequency
    frame_saving_frequency = 10 ** (order_of_magnitude - 1)

    if frame % frame_saving_frequency == 0 or frame == 1:
        filename = f"/tmp/frame_{frame}.png"
        plt.savefig(filename)
        frame_images.append(Image.open(filename))

# Create the GIF with a fixed frame duration
final_gif_path = "cumulative_letter_frequency_numbers.gif"
fixed_duration = 200  # Fixed duration in milliseconds for each frame
frame_images[0].save(
    final_gif_path,
    save_all=True,
    append_images=frame_images[1:],
    duration=fixed_duration,
    loop=0
)

print("Animation saved.")
