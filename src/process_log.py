from heapq import heappush, heappop, heapify, heappushpop
from datetime import datetime,timedelta, time
import time
start_time = time.time()

ips = {}
res = {}
tim = {}
heap_ips = []
heap_bandwidth = []
heap_timestamp = []
tim_list = []


def updateheap(freq_dict, entity, heap):
    index = -1
    for i in range(0, len(heap)):
        if heap[i][1] == entity:
            index = i
            break

    if index != -1:
        heap[index] = (freq_dict[entity], entity)
        heapify(heap)
    else:
        if len(heap) == 10:
            heappushpop(heap, (freq_dict[entity], entity))
        else:
            heappush(heap, (freq_dict[entity], entity))

class window:
    sum = 0
    timestamps = []

w = window()

fail_counts = {}
blocked = {}

blockedfile = open('log_output/blocked.txt', 'w')
hourdelta = timedelta(minutes=59)
timestamp_format = "%d/%b/%Y:%H:%M:%S -0400"
timestamp = None
with open('log_input/log.txt', 'r') as f:
    for line in f:
        split = line.split(' ')
        hostname = split[0]
        resource = split[6]

        s = split[3].replace('[','') + ' ' + split[4].replace(']','')
        timestamp = datetime.strptime(s, timestamp_format)

        # print split
        replycode = split[-2]

        if resource in blocked:
            if timestamp < blocked[resource] + timedelta(minutes=5):
                blockedfile.write(line)
            else:
                del blocked[resource]

        if resource == '/login':
            if replycode == '401':
                if resource not in fail_counts:
                    fail_counts[resource] = [timestamp]
                else:
                    stamps = fail_counts[resource]
                    copy = [x for x in stamps]

                    for i in range(len(copy)):
                        if copy[i] < timestamp - timedelta(seconds=20):
                            stamps.remove(copy[i])

                    stamps.append(timestamp)
                    fail_counts[resource] = stamps
                    if len(stamps) == 3:
                        blocked[resource] = timestamp

            elif replycode != '401' and resource in fail_counts:
                del fail_counts[resource]

        if timestamp not in tim:
            tim[timestamp] = 1
            tim_list.append(timestamp)
        else:
            tim[timestamp] += 1

        if hostname not in ips:
            ips[hostname] = 0
        ips[hostname] += 1

        if resource not in res:
            res[resource] = 0
        if split[-1] != '-\n':
            res[resource] += int(split[-1].replace('\n', ''))

        updateheap(ips, hostname, heap_ips)
        updateheap(res, resource, heap_bandwidth)

start = tim_list[0]
last = tim_list[-1] + timedelta(minutes=60)

w = window()

t = start
while t < start + timedelta(minutes=59):
    if t in tim:
        w.sum += tim[t]
        w.timestamps.append(t)
    t = t + timedelta(seconds=1)

td = {}
window_start = start
window_end = start + timedelta(minutes=59)
while window_end <= last:
    td[window_start] = w.sum
    updateheap({window_start: w.sum}, window_start, heap_timestamp)

    if window_start in tim:
        w.sum = w.sum - tim[window_start]
    if window_end in tim:
        w.sum = w.sum + tim[window_end]
    window_start = window_start + timedelta(seconds=1)
    window_end = window_end + timedelta(seconds=1)


l = []
for i in range(len(heap_ips)):
    e = heappop(heap_ips)
    s = e[1] + ',' +str(e[0])
    l = [s] + l

with open('log_output/hosts.txt', 'w') as f:
    for i in l:
        f.write(i + '\n')

l = []
for i in range(len(heap_bandwidth)):
    e = heappop(heap_bandwidth)
    s = e[1]
    l = [s] + l

with open('log_output/resources.txt', 'w') as f:
    for i in l:
        f.write(i + '\n')
        # print i

l = []
for i in range(len(heap_timestamp)):
    e = heappop(heap_timestamp)
    s = str(e[1].strftime(timestamp_format)) + ',' +str(e[0])
    l = [s] + l


with open('log_output/hours.txt', 'w') as f:
    for i in l:
        f.write(i + '\n')
        # print i

print("--- Execution time %s seconds ---" % (time.time() - start_time))