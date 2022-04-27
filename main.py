import time
import aiohttp
import asyncio
import pandas as pd
import os

start_time = time.time()

csv_file = 'addresses.csv'
json_file = 'addresses.txt'

postcode_locality = (
    'ATD', 'BBG', 'BKR', 'BML', 'BRG', 'BZN', 'CBD', 'DGL', 'FGR', 'FNT', 'FRN', 'GDJ', 'GHR', 'GRB', 'GSM', 'GSR',
    'GXQ', 'GZR', 'HMR', 'IKL', 'ISL', 'KCM', 'KKP', 'KKR', 'KMN', 'LJA', 'LQA', 'MDN', 'MEC', 'MFN', 'MGR', 'MLH',
    'MQB', 'MRS', 'MSD', 'MSK', 'MST', 'MTF', 'MTP', 'MXK', 'MXR', 'NDR', 'NXR', 'PBK', 'PLA', 'PTA', 'QLA', 'QRD',
    'QRM', 'RBT', 'SCM', 'SFI', 'SGN', 'SGW', 'SLC', 'SLM', 'SLZ', 'SNT', 'SPB', 'STJ', 'SPK', 'SVR', 'SWQ', 'TXN',
    'VCT', 'VLT', 'XBX', 'XJR', 'XLN', 'XRA', 'XWK', 'ZBB', 'ZBG', 'ZBR', 'ZRQ', 'ZTN')


async def get_address(locality, number, session):
    url = (f'https://www.maltapost.com/AddressPublicApi//api/v1/Address/Search?'
           f'query={locality}%20{number}&maxResult=1000')
    response = await session.request(method='GET', url=url)
    return response


async def save_address(locality, number, session):
    response = await get_address(locality, number, session)
    response_json = await response.text()
    postcode = locality + " " + str(number)
    if postcode in response_json:
        with open(json_file, 'a') as file:
            file.write(response_json)
            file.close()


async def main():
    async with aiohttp.ClientSession() as session:
        for locality in postcode_locality:
            print(f"Collecting addresses for locality with postcode {locality}...")
            run_time = time.time()
            await asyncio.gather(*[save_address(locality, number, session) for number in range(1000, 10000)])
            print(f'Address for locality with postcode {locality} collected successfully.')
            print('Finished in: ' + str(time.time() - run_time) + ' seconds\n')
            time.sleep(20)


asyncio.run(main())

# Opens the addresses.txt file which contains multiple JSON arrays
# and saves its contents into the addresses variable.
with open(json_file) as a:
    addresses = a.read()
    a.close()

# # Turns multiple JSON arrays into one by removing the closing and opening
# # square brackets of each consecutive array.
addresses = addresses.replace('][', ',')

# Converts the JSON file int a CSV file using the Pandas package.
df = pd.read_json(addresses)
df.to_csv(csv_file, index=None)
# Opens the new csv file
df = pd.read_csv(csv_file, dtype={'flatNo': str})

# Removes the rank and id columns and afterwards removes any duplicate rows
df.drop(['rank', 'id'], inplace=True, axis=1)
df.drop_duplicates(subset=None, inplace=True)
# Saves the cleaned up csv file
df.to_csv(csv_file, index=False)

os.remove(json_file)

end_time = time.time()
print('Finished in: ' + str(end_time - start_time) + ' seconds')
