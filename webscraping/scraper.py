#import boto3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import pandas as pd
import newspaper

#ec2 = boto3.resource('ec2')
#instance = ec2.create_instances(
#    ImageId='ami-0603cbe34fd08cb81',
#    MinCount=1,
#    MaxCount=1,
#    InstanceType='t2.micro'
#)

#print(instance[0].id)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
client = gspread.authorize(creds)

sh = client.open('news_outlets')
worksheet_list = sh.worksheets()

# start at 3 because first 2 rows are headers,
starting_row = 3
outlet_column = 1
url_column = 3

for spreadsheet in worksheet_list:
    index = 0
    begin = 0
    print('Beginning sheet', index,  ': ', spreadsheet.title)

    num_rows = int(spreadsheet.row_count)
    num_cols = spreadsheet.col_count
    print('number of rows:', num_rows)
    print('number of columns:', num_cols)

    csv_cols = ["outlet", "url", "top_image", "title", "authors",
            "publish_date", "keywords", "summary", "text"]

    # +1 because 2nd parameter is not inclusive
    for row_index in range(starting_row, num_rows + 1):
        csv_data = []
        # begin = 0

        outlet = spreadsheet.cell(row_index, outlet_column).value
        url = spreadsheet.cell(row_index, url_column).value
        source = newspaper.build(url, memoize_articles=False)

        for article in source.articles:
            try:
                article.download()
                article.parse()
                article.nlp()
            except newspaper.article.ArticleException:
                pass
            csv_data.append([source.brand, article.url, article.top_image, article.title, article.authors,
                        article.publish_date, article.keywords, article.summary, article.text])

        sourceset = pd.DataFrame(data=csv_data, columns=csv_cols)
        if begin == 0:
            sourceset.to_csv('scraped_articles/' + spreadsheet.title + '.csv')
            begin = 1
        else:
            sourceset.to_csv('scraped_articles/' + spreadsheet.title + '.csv', header=None, mode="a")
        
        print(outlet, 'outlet done')
    print(spreadsheet.title, 'sheet done')
print('all done')

