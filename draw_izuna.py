import os
import subprocess
from datetime import datetime, timedelta

# ==========================================
# 설정 영역
# ==========================================
GIT_EMAIL = "your_email@example.com"  # 깃허브 이메일
GIT_NAME = "Your Name"                # 깃허브 이름

# 날짜 설정: 2024년 1월 1일이 포함된 주(Week)의 일요일을 찾습니다.
# 2024년 1월 1일은 월요일이므로, 기준점(start_date)은 2023년 12월 31일(일요일)이 됩니다.
target_start = datetime(2024, 1, 1) # 시작하고 싶은 날짜

# 해당 날짜가 속한 주의 일요일 구하기 (Python은 월=0...일=6)
# weekday()가 6(일요일)이 아니면 그만큼 날짜를 뺍니다.
# (Monday(0) -> -1일 -> Sunday)
days_to_subtract = (target_start.weekday() + 1) % 7
start_date = target_start - timedelta(days=days_to_subtract)

# ==========================================
# 글자 도트 매트릭스 (7행 높이: 일~토)
# ==========================================
letters = {
    'i': [
        [0], # 일 (12/31)
        [1], # 월 (1/1 - 여기에 첫 점이 찍힘!)
        [0], # 화
        [1], # 수
        [1], # 목
        [1], # 금
        [1], # 토
    ],
    'z': [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
    ],
    'u': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
    ],
    'n': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
    ],
    'a': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
    ],
    ' ': [[0]*7]
}

word_map = []
target_word = "izuna"

for char in target_word:
    if char in letters:
        shape = letters[char]
        width = len(shape[0])
        for col in range(width):
            column_data = [row[col] for row in shape]
            word_map.append(column_data)
        word_map.append([0]*7)

# ==========================================
# 실행 로직
# ==========================================
print(f"Grid Start Date (Sunday): {start_date.strftime('%Y-%m-%d')}")
print(f"Drawing starts effectively from: {target_start.strftime('%Y-%m-%d')}")

current_date = start_date

for column in word_map:
    for day_offset, pixel in enumerate(column):
        if pixel == 1:
            commit_date = current_date + timedelta(days=day_offset)
            date_str = commit_date.strftime("%Y-%m-%d %H:%M:%S")

            with open("pixel_art.txt", "a") as f:
                f.write(f"Commit for {date_str}\n")

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str

            subprocess.run(["git", "add", "pixel_art.txt"], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Pixel {date_str}"],
                env=env,
                check=True,
                stdout=subprocess.DEVNULL
            )

    current_date += timedelta(days=7)

print("Done! Push to GitHub to see the results in 2024.")