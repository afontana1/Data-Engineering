import pandas as pd
from index import RetailPriceProcessed, RetailPrices, Session

with Session.begin() as db:
    data = pd.read_csv("retail_price.csv")
    for index, row in data.iterrows():
        retail_prices = RetailPrices(
            product_id=row[0],
            product_category_name=row[1],
            month_year=row[2],
            qty=row[3],
            total_price=row[4],
            freight_price=row[5],
            unit_price=row[6],
            product_name_lenght=row[7],
            product_description_lenght=row[8],
            product_photos_qty=row[9],
            product_weight_g=row[10],
            product_score=row[11],
            customers=row[12],
            weekday=row[13],
            weekend=row[14],
            holiday=row[15],
            month=row[16],
            year=row[17],
            s=row[18],
            volume=row[19],
            comp_1=row[20],
            ps1=row[21],
            fp1=row[22],
            comp_2=row[23],
            ps2=row[24],
            fp2=row[25],
            comp_3=row[26],
            ps3=row[27],
            fp3=row[28],
            lag_price=row[29],
        )
        db.add(retail_prices)


with Session.begin() as db:
    data = pd.read_csv(
        "/Users/ayushsingh/Desktop/MLProjectPackages/retail-price-optimization/data/df_with_significant_vars.csv"
    )
    print(data)
    for index, row in data.iterrows():
        print(row)
        retail_prices_with_sig_vars = RetailPriceProcessed(
            total_price=row[0],
            unit_price=row[1],
            customers=row[2],
            s=row[3],
            comp_2=row[4],
            qty=row[5],
        )
        db.add(retail_prices_with_sig_vars)
