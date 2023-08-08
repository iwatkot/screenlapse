import os
import cv2
import pyautogui
from time import sleep

ABOSOLUTE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(ABOSOLUTE_PATH)
SCREENSHOT_DIR = os.path.join(CURRENT_DIR, "screenshots")
VIDEO_DIR = os.path.join(CURRENT_DIR, "videos")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
print(f"Screenshot directory: {SCREENSHOT_DIR}")


def get_session_dir():
    subdirectories = [x[0] for x in os.walk(SCREENSHOT_DIR) if x[0] != SCREENSHOT_DIR]
    subdirectory_counter = len(subdirectories)

    while True:
        subdirectory = os.path.join(
            SCREENSHOT_DIR, f"session_{str(subdirectory_counter).zfill(3)}"
        )

        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory)
            print(f"Session directory: {subdirectory}")
            return subdirectory
        else:
            subdirectory_counter += 1


def start_screenshots(timer: int, stop: int = None):
    session_dir = get_session_dir()
    print(f"Starting screenshots with timer: {timer} seconds in {session_dir}")

    counter = 0
    if not stop:
        print("Stop is not defined, will run forever, press CTRL+C to stop")
        while True:
            save_path = os.path.join(session_dir, f"{str(counter).zfill(5)}.png")
            save_screenshot(save_path)
            counter += 1
            sleep(timer)

    else:
        print(f"Will stop after {stop} screenshots")
        for _ in range(stop):
            save_path = os.path.join(session_dir, f"{str(counter).zfill(5)}.png")
            save_screenshot(save_path)
            counter += 1
            sleep(timer)


def save_screenshot(save_path: str):
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    print(f"Screenshot saved: {save_path}")


def create_timelapse(session_number: int = None):
    if not session_number:
        subdirectories = [
            x[0] for x in os.walk(SCREENSHOT_DIR) if x[0] != SCREENSHOT_DIR
        ]
        last_session = sorted(subdirectories)[-1]
        session_number = int(last_session.split("_")[-1])

    FRAMERATE = 30

    session_dir = os.path.join(
        SCREENSHOT_DIR, f"session_{str(session_number).zfill(3)}"
    )

    print(f"Creating timelapse for session: {session_dir}")

    ordered_pngs = sorted(
        [os.path.join(session_dir, x) for x in os.listdir(session_dir)]
    )

    print(f"Found {len(ordered_pngs)} screenshots")

    first_image = cv2.imread(ordered_pngs[0])
    height, width, _ = first_image.shape
    FRAME_SIZE = (width, height)

    print(f"Video dimensions: {FRAME_SIZE}")

    output_path = os.path.join(VIDEO_DIR, f"session_{str(session_number).zfill(3)}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, FRAMERATE, FRAME_SIZE)

    print(f"Saving video to: {output_path}")

    for png in ordered_pngs:
        img = cv2.imread(png)
        out.write(img)

    out.release()

    print(f"Video saved: {output_path}")
    return output_path


if __name__ == "__main__":
    TIMER = 1
    STOP = None
    try:
        start_screenshots(timer=TIMER, stop=STOP)
    except KeyboardInterrupt:
        print("App was stopped by user, creating timelapse...")
        create_timelapse()
        print("Script finished")
