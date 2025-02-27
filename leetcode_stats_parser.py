import requests
import re
svg_data = requests.get('https://leetcode-stats.vercel.app/api?username=ulansyn&theme=Light')
svg_data = svg_data.text

pattern_easy = r'Easy Questions Solved:</text>\s*<text class="stat easy" x="200" y="12.5">(\d+)/\d+'
pattern_medium = r'Medium Questions Solved:</text>\s*<text class="stat medium" x="200" y="12.5">(\d+)/\d+'
pattern_hard = r'Hard Questions Solved:</text>\s*<text class="stat hard" x="200" y="12.5">(\d+)/\d+'

matches_easy = re.findall(pattern_easy, svg_data)
matches_medium = re.findall(pattern_medium, svg_data)
matches_hard = re.findall(pattern_hard, svg_data)

easy_solved = int(matches_easy[0]) if matches_easy else 0
medium_solved = int(matches_medium[0]) if matches_medium else 0
hard_solved = int(matches_hard[0]) if matches_hard else 0

total_solved = easy_solved + medium_solved + hard_solved

print("Total Easy Questions Solved:", easy_solved)
print("Total Medium Questions Solved:", medium_solved)
print("Total Hard Questions Solved:", hard_solved)
print("Total Questions Solved:", total_solved)
