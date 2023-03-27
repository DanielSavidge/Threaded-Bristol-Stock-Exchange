import re
import os
import csv
import pandas as pd

if __name__ == "__main__":
    result_folders = ["results"]
    table = pd.DataFrame(columns=["Trader", "Profit", "Market Share"])

    for folder_path in result_folders:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path) as csvfile:
                    csv_reader = csv.reader(csvfile, delimiter=',')

                    pattern = r'(\d+)-(\d+)-(\d+)-(\d+)-(\d+)-(\d+)'
                    match = re.match(pattern,filename)
                    num_traders = [int(x) for x in match.groups()]
                    all_traders = ["ZIC","ZIP","GDX","AA","GVWY","SHVR"]
                    trader_names = [trader for trader, num in zip(all_traders, num_traders) if num != 0]

                    trader_profit = [0] * len(trader_names)
                    trader_trades = [0] * len(trader_names)

                    # Iterate over the rows of the CSV file to extract the total profit of each trader and create a table with market share
                    num_simulations = 0 
                    for row in csv_reader:
                        num_simulations+=1
                        trial_id = row[0]
                        for i, trader_name in enumerate(trader_names):
                            trader_profit[i] += float(row[1+i*7+3])
                            trader_trades[i] += float(row[1+i*7+4])

                    # Add the total profit and market share for each trader to the table
                    for i, trader_name in enumerate(trader_names):
                        profit = trader_profit[i]/num_simulations
                        trader_index = all_traders.index(trader_name)
                        trader_count = num_traders[trader_index]
                        market_share = 100*num_traders[trader_index] / sum([i for i in num_traders])
                        table = table.append({"Trader": trader_name, "Profit": profit, "Market Share": market_share}, ignore_index=True)

        # Group the table by trader name and market share and sum the profits
        table = table.groupby(["Trader", "Market Share"]).agg({"Profit": "sum"}).reset_index()

        # Save the table to a CSV file
        table.to_csv("trader_profit_table_sum.csv", index=False)
