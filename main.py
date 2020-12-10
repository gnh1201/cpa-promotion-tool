#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read_linkprice(filename):
    return pd.read_excel(
        filename,
        sheet_name = 'Sheet1',
        header = 0,
        names = [
            'id',
            'sitename',
            'category',
            'status',
            'url',
            'original_url',
            'valid',
            'program_name',
            'program_description',
            'accumulate_type',
            'is_reward',
            'is_mobile',
            'start_date',
            'end_date',
            'commision'
        ],
        dtype = {
            'id': str,
            'sitename': str,
            'category': str,
            'status': str,
            'url': str,
            'original_url': str,
            'valid': str,
            'program_name': str,
            'program_description': str,
            'accumulate_type': str,
            'is_reward': str,
            'is_mobile': str,
            'start_date': str,
            'end_date': str,
            'commision': str
        },
        #index_col = 'id',
        na_values = 'NaN',
        thousands = ',',
        #nrows = 10,
        comment = '#'
    )

def tokenize(text):
    return (text.replace('/', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ')).split(' ')

def writePromotions(promotions):
    contents = '<?xml version="1.0" encoding="UTF-8"?>\n'
    contents += '<Promotions start="0" num="' + str(len(promotions)) + '" total="' + str(len(promotions)) + '">\n';
    for promotion in promotions:
        contents += '  <Promotion id="' + promotion['id'] + '" queries="' + promotion['queries'] + '" title="' + promotion['title'] + '" url="' + promotion['url'] + '" is_regex="false" enabled="true" description="' + promotion['description'] + '" />\n'
    contents += '</Promotions>'

    f = open("promotions.xml", 'w', encoding='utf8')
    f.write(contents)
    f.close()

def main(args):
    promotions = []

    # Linkprice CPS
    df_cps_linkprice = read_linkprice('data/linkprice_cps.xlsx')
    df_cps_linkprice.drop_duplicates(subset='id', keep = 'first', inplace = True)
    for index, row in df_cps_linkprice.iterrows():
        if (row['status'] == "승인"):
            m = hashlib.sha1()
            m.update(row['id'].encode('utf-8'))
            id = m.hexdigest()[0:16]
            queries = ','.join(list(filter(None, tokenize(row['id'].strip() + ' ' + row['sitename'].strip() + ' ' + row['category'].strip()))))
            title = row['sitename']
            url = row['url'].replace('&', '&amp;')
            description = row['category'].strip()

            promotions.append({
                'id': id,
                'queries': queries,
                'title': title,
                'url': url,
                'is_regex': False,
                'enabled': True,
                'description': description
            })

    # Linkprice CPA
    df_cps_linkprice = read_linkprice('data/linkprice_cpa.xlsx')
    df_cps_linkprice.drop_duplicates(subset='id', keep = 'first', inplace = True)
    for index, row in df_cps_linkprice.iterrows():
        if (row['status'] == "승인"):
            m = hashlib.sha1()
            m.update(row['id'].encode('utf-8'))
            id = m.hexdigest()[0:16]
            queries = ','.join(list(filter(None, tokenize(row['id'].strip() + ' ' + row['sitename'].strip() + ' ' + row['category'].strip()))))
            title = row['sitename']
            url = row['url'].replace('&', '&amp;')
            description = row['category'].strip()

            promotions.append({
                'id': id,
                'queries': queries,
                'title': title,
                'url': url,
                'is_regex': False,
                'enabled': True,
                'description': description
            })

    writePromotions(promotions)

    return 0

if __name__ == '__main__':
    import sys
    import os
    import pandas as pd
    import hashlib
    sys.exit(main(sys.argv))
