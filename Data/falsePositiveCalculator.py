import pandas as pd
import csv

read_file = '/Users/mingjun.lim/Documents/youtubeScraper/Data/secondRound.csv'
df = pd.read_csv(read_file)
fake_count = 0
pred_count = 0
index = 0
for item in df['pred_threat']:
    if item == 'HIG' and df['threat'][index] != 'HIG':
        fake_count += 1
    index += 1

index = 0
for item in df['pred_threat']:
    if item == 'HIG':
        pred_count += 1
    index += 1

print(fake_count)
print(pred_count)
print(1 - fake_count/pred_count)