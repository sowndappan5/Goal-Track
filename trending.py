import pandas as pd

trending_dataset = pd.read_excel("trending_domains.xlsx")
trending_domains = trending_dataset['Trending domains'].tolist()

def trend():
    trending_domains = trending_dataset.to_dict(orient='records')
    return trending_domains