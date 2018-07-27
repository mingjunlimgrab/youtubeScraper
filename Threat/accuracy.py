def accuracy(original_file, predictions_file):
    df1 = pd.read_csv(original_file)
    df2 = pd.read_csv(predictions_file)
    original_high = 0
    for item in df1['threat']:
        if item == 'HIG':
            original_high += 1
    correct_high = 0
    for index in range(len(df2['threat'])):
        if df2['threat'][index] == df2['pred_threat'][index]:
            correct_high += 1
    acc = correct_high / original_high
    print(acc)
