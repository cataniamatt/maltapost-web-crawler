# MaltaPost postcode finder web crawler
This is a script that gets all of the addresses stored within the MaltaPost address database. This translates to roughly all of the addresses in Malta.

## Functionality of the postcode finder
The MaltaPost postcode finder API returns a list of addresses that are found within any particular postcode. If the postcode does not exist or is incorrect, the API returns a list of all the addresses located within the closest existing postcode to the one entered. 

## Format of Maltese postcodes
Maltese postcodes are a string of 7 characters in which the first three characters are letters that abbreviate the locality name and the other 4 characters are a number ranging from 1000 till 9999, both numbers included. Below are all the possible postcode prefixes:

```
    'ATD', 'BBG', 'BKR', 'BML', 'BRG', 'BZN', 'CBD', 'DGL', 'FGR', 'FNT', 'FRN', 'GDJ', 'GHR', 'GRB', 'GSM', 'GSR',
    'GXQ', 'GZR', 'HMR', 'IKL', 'ISL', 'KCM', 'KKP', 'KKR', 'KMN', 'LJA', 'LQA', 'MDN', 'MEC', 'MFN', 'MGR', 'MLH',
    'MQB', 'MRS', 'MSD', 'MSK', 'MST', 'MTF', 'MTP', 'MXK', 'MXR', 'NDR', 'NXR', 'PBK', 'PLA', 'PTA', 'QLA', 'QRD',
    'QRM', 'RBT', 'SCM', 'SFI', 'SGN', 'SGW', 'SLC', 'SLM', 'SLZ', 'SNT', 'SPB', 'STJ', 'SPK', 'SVR', 'SWQ', 'TXN',
    'VCT', 'VLT', 'XBX', 'XJR', 'XLN', 'XRA', 'XWK', 'ZBB', 'ZBG', 'ZBR', 'ZRQ', 'ZTN'
```

## How the script works
This Python script loops over the list of all the Maltese postcode prefixes that exist and sends a request to the API for each possible postcode number. Example, for a locality named Birkirkara which has a postcode prexis of BKR, the script starts by getting the addresses in BKR1000, then it proceeds to get all the addresses in postcode BKR1001, and it continues to increment until it reaches BKR9999. At this stage, the script then moves to the next locality by changing the postcode prexis.

### HTTP requests
The script uses aiohttp to send the HTTP GET requests in conjunction with Asyncio, which allows the script to send multiple HTTP GET requests to the API asynchroniously.
