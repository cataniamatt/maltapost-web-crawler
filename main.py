from pymongo import MongoClient
import time
import aiohttp
import asyncio

CONNECTION_STRING = "mongodb://admin:password@localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.addresses
collection = db.malta

start_time = time.time()

addresses = []

postcode_locality = (
    'ATD', 'BBG', 'BKR', 'BML', 'BRG', 'BZN', 'CBD', 'DGL', 'FGR', 'FNT', 'FRN', 'GDJ', 'GHR', 'GRB', 'GSM', 'GSR',
    'GXQ', 'GZR', 'HMR', 'IKL', 'ISL', 'KCM', 'KKP', 'KKR', 'KMN', 'LJA', 'LQA', 'MDN', 'MFN', 'MGR', 'MLH', 'MQB', 'MRS', 'MSD', 'MSK', 'MST', 'MTF', 'MTP', 
    'MXK', 'MXR', 'NDR', 'NXR', 'PBK', 'PLA', 'PTA', 'QLA', 'QRD',
    'QRM', 'RBT', 'SCM', 'SFI', 'SGN', 'SGW', 'SLC', 'SLM', 'SLZ', 'SNT', 'SPB', 'STJ', 'SPK', 'SVR', 'SWQ', 'TXN',
    'VCT', 'VLT', 'XBX', 'XJR', 'XLN', 'XRA', 'XWK', 'ZBB', 'ZBG', 'ZBR', 'ZRQ', 'ZTN')

async def get_address(locality, number, session):
    url = (f'https://www.maltapost.com/AddressPublicApi//api/v1/Address/Search?'
           f'query={locality}%20{number}&maxResult=1000')
    response = await session.request(method='GET', url=url)
    return response

async def save_address(locality, number, session):
    response = await get_address(locality, number, session)
    response = await response.json()
    postcode = locality + " " + str(number)
    for address in range(len(response)):
        if response[address]["postCode"] == postcode:
            addresses.append(response[address])
            
async def main():
    async with aiohttp.ClientSession() as session:
        for locality in postcode_locality:
            global addresses
            addresses = []
            print(f"Collecting addresses for locality with postcode {locality}...")
            run_time = time.time()
            await asyncio.gather(*[save_address(locality, number, session) for number in range(1000, 10000)])
            print(f'Addresses for locality with postcode {locality} collected successfully.')
            print('Inserting addresses into database.')
            collection.insert_many(addresses)
            print('Finished in: ' + str(time.time() - run_time) + ' seconds\n')

asyncio.run(main())

end_time = time.time()
print('Finished in: ' + str(end_time - start_time) + ' seconds')
