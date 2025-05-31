import json
import argparse
from datetime import datetime, timedelta

def parse_time(t):
    return datetime.strptime(t, "%H:%M")

def minutes(td):
    return td.seconds // 60

def format_time(dt):
    return dt.strftime("%H:%M")

def solve(data):
    work_start = parse_time(data['work_start'])
    work_end = parse_time(data['work_end'])

    customers = data['customers']
    n = len(customers)
    # Preprocess customers
    for c in customers:
        c['avail_from'] = parse_time(c['available_from'])
        c['avail_to'] = parse_time(c['available_to'])
        c['duration_td'] = timedelta(minutes=c['visit_duration'])

    travel = data['travel_time'] 

    dp = {}
    parent = {}


    for i, c in enumerate(customers, start=1):
        depart = work_start
        arr = depart + timedelta(minutes=travel[0][i])
        if arr <= c['avail_to']:
            start = max(arr, c['avail_from'])
            finish = start + c['duration_td']
            if finish <= c['avail_to'] and finish <= work_end:
                mask = 1 << (i-1)
                dp[(mask, i)] = finish
                parent[(mask, i)] = (0, 0)  # from depot


    for mask in range(1, 1<<n):
        for last in range(1, n+1):
            if not (mask & (1<<(last-1))): continue
            key = (mask, last)
            if key not in dp: continue
            finish_prev = dp[key]
            for j in range(1, n+1):
                bit = 1<<(j-1)
                if mask & bit: continue
                c = customers[j-1]
                arr = finish_prev + timedelta(minutes=travel[last][j])
                if arr <= c['avail_to']:
                    start = max(arr, c['avail_from'])
                    finish = start + c['duration_td']
                    if finish <= c['avail_to'] and finish <= work_end:
                        new_key = (mask | bit, j)
                        if new_key not in dp or finish < dp[new_key]:
                            dp[new_key] = finish
                            parent[new_key] = key


    best_value = 0
    best_key = None
    for (mask, last), finish in dp.items():
        value = sum(customers[i]['visit_value'] for i in range(n) if mask & (1<<i))
        if value > best_value:
            best_value = value
            best_key = (mask, last)


    route = []
    key = best_key
    if key:
        while key and key in parent:
            mask, last = key
            if last == 0: break
            route.append(last-1)
            key = parent[key]
        route = list(reversed(route))

    # Prepare output
    output = {'best_value': best_value, 'route': route, 'route_times': []}
    time_cursor = work_start
    prev_idx = 0
    for idx in route:
        j = idx+1
        arr = time_cursor + timedelta(minutes=travel[prev_idx][j])
        start = max(arr, customers[idx]['avail_from'])
        finish = start + customers[idx]['duration_td']
        output['route_times'].append({
            'customer': customers[idx]['id'],
            'arrival': format_time(arr),
            'start': format_time(start),
            'finish': format_time(finish)
        })
        time_cursor = finish
        prev_idx = j

    return output


def main():
    parser = argparse.ArgumentParser(
        description='Orienteering solver for ERP marketing visits')
    parser.add_argument('input', help='Path to input JSON file')
    parser.add_argument('output', help='Path to write result JSON')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        data = json.load(f)

    result = solve(data)

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Result written to {args.output}")

if __name__ == '__main__':
    main()
