import subprocess
import os
import sys
import time
import json

# ========================================
# find vlc
# ========================================
def find_vlc():
    paths = [
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

VLC = find_vlc()
if not VLC:
    print("ERROR: VLC not found. Please install VLC.")
    input("Press Enter to exit...")
    sys.exit(1)

# ========================================
# SEARCH VIDEO
# ========================================
def search_video(query, offset=0, limit=20):
    cmd = [
        "yt-dlp.exe",
        f"ytsearch{limit+offset}:{query}",
        "--skip-download",
        "--print-json"
    ]

    results = []
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                info = json.loads(line)
                title = info.get("title")
                url = info.get("webpage_url")
                if title and url:
                    results.append((title, url))
            except:
                continue
        proc.wait()
    except Exception as e:
        print("Search failed:", e)
    
    return results[offset:offset+limit]

# ========================================
# PLAY VIDEO
# ========================================
def play(url, height):
    fmt = f"best[height<={height}]"
    cmd = [
        "yt-dlp.exe",
        "-f", fmt,
        "-o", "-",
        url
    ]

    vlc = subprocess.Popen([VLC, "-"], stdin=subprocess.PIPE)
    ytdlp = subprocess.Popen(cmd, stdout=vlc.stdin)
    return vlc, ytdlp

# ========================================
# MAIN MENU
# ========================================
def main():
    while True:
        os.system("cls")
        print("=== YouTubeLiteClient ===")
        print("1) Search video")
        print("2) Paste link")
        print("q) Quit")
        choice = input("> ").strip().lower()

        if choice == "q":
            break
        elif choice == "2":
            url = input("Link: ").strip()
        elif choice == "1":
            query = input("Search: ").strip()
            offset = 0
            while True:
                results = search_video(query, offset, limit=20)
                if not results:
                    print("No results found.")
                    input("Press Enter to continue...")
                    break

                print(f"\nResults {offset+1}-{offset+len(results)}:")
                for i, (title, _) in enumerate(results, start=1):
                    print(f"{i}) {title}")

                print("\nn = next page, b = previous page, q = quit search")
                sel = input("Choose a number or command: ").strip().lower()

                if sel == "n":
                    offset += 20
                    continue
                elif sel == "b":
                    offset = max(0, offset - 20)
                    continue
                elif sel == "q":
                    break
                else:
                    try:
                        sel = int(sel) - 1
                        if sel < 0 or sel >= len(results):
                            print("Invalid selection.")
                            input("Press Enter to continue...")
                            continue
                        url = results[sel][1]
                        break
                    except:
                        print("Invalid input.")
                        input("Press Enter to continue...")
                        continue
        else:
            continue

       
        print("\nResolution:")
        print("1) 360p (recommended)")
        print("2) 480p")
        print("3) 720p (may lag)")
        print("4) 1080p (may lag a lot)")
        res_choice = input("> ").strip()
        if res_choice == "1":
            height = 360
        elif res_choice == "2":
            height = 480
        elif res_choice == "3":
            height = 720
        elif res_choice == "4":
            height = 1080
        else:
            height = 360

        
        print("\nLoading...")
        vlc, ytdlp = play(url, height)
        print("\nPress ENTER to stop playback and return to home")
        input()
        vlc.terminate()
        ytdlp.terminate()
        time.sleep(1)

# ========================================
# RUN
# ========================================
if __name__ == "__main__":
    main()

