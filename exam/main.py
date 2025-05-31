import os
import random

try:
    from rich import print
    import heapq
    from bitarray import bitarray
except:
    os.system('pip install -r requirements.txt')
    from rich import print
    import heapq
    from bitarray import bitarray


print("""
[bold green]

 _____                      __  __
| ____|_  ____ _ _ __ ___   \ \/ /
|  _| \ \/ / _` | '_ ` _ \   \  / 
| |___ >  < (_| | | | | | |  /  \ 
|_____/_/\_\__,_|_| |_| |_| /_/\_\

    [/bold green]
      
""")





DATA_FILE = os.path.join(os.path.dirname(__file__), 'responses.bin')

class BitStorage:
    def __init__(self, filename):
        self.filename = filename
        self.total = 100_000 * 10 * 5 
        self.bits = bitarray(self.total * 2)
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.bits.fromfile(f)
            if len(self.bits) < self.total * 2:
                self.bits.extend([0] * (self.total * 2 - len(self.bits)))
        else:
            self.bits.setall(0)

    def reset(self):
        self.bits.setall(0)

    def _index(self, pid, tid, lid):
        if not (1 <= pid <= 100_000 and 1 <= tid <= 10 and 1 <= lid <= 5):
            raise ValueError("شناسه‌ها باید در بازه‌های مجاز باشند.")
        linear = ((pid - 1) * 10 + (tid - 1)) * 5 + (lid - 1)
        return linear * 2

    def set_color(self, pid, tid, lid, color):
        if not (0 <= color <= 3):
            raise ValueError("رنگ باید بین 0 و 3 باشد.")
        i = self._index(pid, tid, lid)
        bits = bitarray(format(color, '02b'))
        self.bits[i:i+2] = bits

    def get_color(self, pid, tid, lid):
        i = self._index(pid, tid, lid)
        return int(self.bits[i:i+2].to01(), 2)

    def flush(self):
        with open(self.filename, 'wb') as f:
            self.bits.tofile(f)


def generate_random_data(storage):
    print("در حال تولید داده‌ی تصادفی برای 100,000 شرکت‌کننده...")
    storage.reset()
    for pid in range(1, 100_001):
        for tid in range(1, 11):
            for lid in range(1, 6):
                storage.set_color(pid, tid, lid, random.randint(0, 3))
    storage.flush()
    print("تولید و ذخیره‌سازی تکمیل شد.")


def top_blue(storage, tid, lid, N):
    blues = []
    for pid in range(1, 100_001):
        if storage.get_color(pid, tid, lid) == 3:
            blues.append(pid)
            if len(blues) >= N:
                break
    return blues

def top_weighted(storage, tid, N):
    heap = []
    for pid in range(1, 100_001):
        score = sum(storage.get_color(pid, tid, lid) * lid for lid in range(1, 6))
        if len(heap) < N:
            heapq.heappush(heap, (score, pid))
        else:
            heapq.heappushpop(heap, (score, pid))
    return sorted(heap, key=lambda x: x[0], reverse=True)

def top_overall(storage, N):
    heap = []
    for pid in range(1, 100_001):
        total = 0
        for tid in range(1, 11):
            total += sum(storage.get_color(pid, tid, lid) * lid for lid in range(1, 6))
        if len(heap) < N:
            heapq.heappush(heap, (total, pid))
        else:
            heapq.heappushpop(heap, (total, pid))
    return sorted(heap, key=lambda x: x[0], reverse=True)

def average_scores(storage):
    avg = {}
    for tid in range(1, 11):
        for lid in range(1, 6):
            s = sum(storage.get_color(pid, tid, lid) for pid in range(1, 100_001))
            avg[(tid, lid)] = s / 100_000
    return avg


def print_menu():
    print("""
[bold green]
1) تولید تصادفی داده‌ها
2) درج/به‌روزرسانی رنگ (participant, test, lesson)
3) N نفر برتر (آبی) یک درس در یک آزمون
4) N نفر برتر در یک آزمون با ضرایب دروس
5) N نفر برتر کل آزمون‌ها
6) میانگین پاسخگویی در هر درس و آزمون
0) خروج
    [/bold green]
""")

def main():
    storage = BitStorage(DATA_FILE)

    while True:
        print_menu()
        print('[bold blue]>> [/bold blue]',end='')
        choice = input("").strip()
        if choice == '1':
            generate_random_data(storage)

        elif choice == '2':
            pid = int(input("participant_id (1-100000): "))
            tid = int(input("test_id (1-10): "))
            lid = int(input("lesson_id (1-5): "))
            color = int(input("color (0=قرمز،1=زرد،2=سبز،3=آبی): "))
            storage.set_color(pid, tid, lid, color)
            storage.flush()
            print("به‌روزرسانی شد.")

        elif choice == '3':
            tid = int(input("test_id (1-10): "))
            lid = int(input("lesson_id (1-5): "))
            N   = int(input("N: "))
            res = top_blue(storage, tid, lid, N)
            print("نتایج:", res)

        elif choice == '4':
            tid = int(input("test_id (1-10): "))
            N   = int(input("N: "))
            res = top_weighted(storage, tid, N)
            print("PID — Score")
            for score, pid in res:
                print(f"{pid}\t— {score}")

        elif choice == '5':
            N   = int(input("N: "))
            res = top_overall(storage, N)
            print("PID — Total Score")
            for score, pid in res:
                print(f"{pid}\t— {score}")

        elif choice == '6':
            avg = average_scores(storage)
            print("آزمون\tدرس\tمیانگین رنگ")
            for (tid, lid), v in sorted(avg.items()):
                print(f"{tid}\t{lid}\t{v:.2f}")

        elif choice == '0':
            print("خداحافظ!")
            break

        else:
            print("انتخاب نامعتبر. دوباره تلاش کنید.")

if __name__ == '__main__':
    main()
