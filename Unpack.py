import os
from Ulog import ULog
import csv
# specifying the path to csv files
try:
    os.mkdir('Ulog')
    os.mkdir('Csv')
except:
    pass
path = r"D:\Хахатон\Журналы полетов\5 (2). Глушение GPS\10.08.2023 (2)"

# csv files in the path 
results = [path+'\\'+each for each in os.listdir(path) if each.endswith('.ulg')]
results
def ulg_unpack(path, out):
    source = ['lat', 'lon', 'rssi', 'noise', 'remote_noise', 'rxerrors', 'fix']
    ulog = ULog(path, None, False)
    data = ulog.data_list
    header = []
    result = {}
    data.sort(key=lambda x: x.name)
    maxlen = 0
    for d in data:
        names = [f.field_name for f in d.field_data]
        names.remove('timestamp')
        names.insert(0, 'timestamp')
        for head in names:
            if head in source:
                if (d.name + '.' + head) not in header: header.append(d.name + '.' + head)
        if len(d.data['timestamp']) > maxlen:
            maxlen = len(d.data['timestamp'])

    for d in data:
        d_keys = [f.field_name for f in d.field_data]
        d_keys.remove('timestamp')
        d_keys.insert(0, 'timestamp')
        for key in d_keys:
            result[d.name + '.' + key] = d.data[key]
    
    
    with open(f'Csv\\{out}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i in range(maxlen):
            row = []
            for head in header:
                if i < len(result[head]):
                    row.append(result[head][i])
                else:
                    row.append('')
            writer.writerow(row)

n = 0
for path in results:
    print(path, n)
    ulg_unpack(path, f'out{n}')
    n+=1