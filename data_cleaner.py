def remove_extra_entities(text):
    ret = []
    longest = max(text, key=len)
    ret.append(longest)
    for i in text:
        if i not in longest:
            ret.append(i)
    return ret


def clean_df(df):
    df['object'] = df['object'].apply(lambda x: ''.join(str(x)))
    df['subject'] = df['subject'].apply(lambda x: ''.join(str(x)))
    df['verb'] = df['verb'].apply(lambda x: ''.join(str(x)))
    df['object'] = df['object'].str.strip('[]')
    df['subject'] = df['subject'].str.strip('[]')
    df['verb'] = df['verb'].str.strip('[]')
    df['object'] = df['object'].str.split(',')
    df['subject'] = df['subject'].str.split(',')
    df['verb'] = df['verb'].str.split(',')
    df['object'] = df['object'].apply(lambda x: remove_extra_entities(x))
    df['subject'] = df['subject'].apply(lambda x: remove_extra_entities(x))
    df['year'] = df['year'].str.rstrip(':')
    new_columns = df['year'].str.split('–', n=1, expand=True)
    df['year from'] = new_columns[0]
    df['year to'] = new_columns[1]
    return df
