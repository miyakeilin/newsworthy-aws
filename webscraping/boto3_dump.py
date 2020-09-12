import boto3
import pandas as pd

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

bucket = 'article-data-newsworthy'
data_key = 'practice_df'
data_location = 's3://{}/{}'.format(bucket, data_key)
df.to_csv(data_location,index=False)