from service.client_mongodb import ClientDB
Table_btc = "influent_bitcoin_account"
Table_all = "influent_account"
ClientDB = ClientDB()

from datetime import datetime

if __name__ == "__main__":
    # all_people = ClientDB.get_all("user_v2")
    # for people in all_people:
    #     print(f'Compute for {people["name"]}')
    #     if (people["kw_app"] > 0 or people["description_kw"] > 0):
    #         ClientDB.import_document(Table_btc, people)
    #         continue
    #     if (people["score"] > 100000):
    #         ClientDB.import_document(Table_all, people)
    date = "Sun Jan 09 00:39:36 +0000 2022"
    datetime = datetime.strptime(date, '%a %b %d %H:%M:%S +%f %Y')
    print(datetime)
