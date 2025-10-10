class LEDClock:
    # LED segments for digits 0-9 (7-seg display encoding)
    digit_led_map = {
        '0': 0b1111110,
        '1': 0b0110000,
        '2': 0b1101101,
        '3': 0b1111001,
        '4': 0b0110011,
        '5': 0b1011011,
        '6': 0b1011111,
        '7': 0b1110000,
        '8': 0b1111111,
        '9': 0b1111011,
    }

    def __init__(self, start_time, cost_hour, cost_minute):
        self.start_hour = int(start_time[:2])
        self.start_minute = int(start_time[3:])
        self.cost_hour = cost_hour
        self.cost_minute = cost_minute

    def led_differs_by_one_segment(self, d1, d2):
        bits1 = self.digit_led_map[d1]
        bits2 = self.digit_led_map[d2]
        xor = bits1 ^ bits2
        return xor != 0 and (xor & (xor - 1)) == 0

    def time_differs_by_one_led(self, t1, t2):
        diffs = 0
        for i in range(5):
            if i == 2:
                continue
            if t1[i] != t2[i]:
                if not self.led_differs_by_one_segment(t1[i], t2[i]):
                    return False
                diffs += 1
                if diffs > 1:
                    return False
        return diffs == 1

    def move_cost(self, h1, m1, h2, m2):
        hour_move = abs(h2 - h1) * 60
        minute_move = abs(m2 - m1)
        return hour_move * self.cost_hour + minute_move * self.cost_minute

    def format_time(self, hour, minute):
        return f"{hour:02d}:{minute:02d}"

    def find_closest_time(self):
        start_time_str = self.format_time(self.start_hour, self.start_minute)
        min_cost = float('inf')
        closest_time = None
        for h in range(1, 13):
            for m in range(60):
                candidate_time = self.format_time(h, m)
                if self.time_differs_by_one_led(start_time_str, candidate_time):
                    cost = self.move_cost(self.start_hour, self.start_minute, h, m)
                    if cost < min_cost or (cost == min_cost and candidate_time < closest_time):
                        min_cost = cost
                        closest_time = candidate_time
        if closest_time is None:
            return "No closest valid time possible"
        else:
            return closest_time


if __name__ == "__main__":
    initial_time = input().strip()
    X, Y = map(int, input().split())
    clock = LEDClock(initial_time, X, Y)
    print(clock.find_closest_time())
