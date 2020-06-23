#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logicalModell
from faker import Faker
import sys

faker = Faker()

def dmlgenerate(amount):
    print("Generating Example Data ...")
    tables = logicalModell.datenbank.tabellen
    for tabl in tables:
        for col in tabl.columns:
            if col.reference == "":
                for i in range(0, int(amount)):
                    if col.clas == "address":
                        col.data.append(faker.address().replace("\n"," "))
                    elif col.clas == "postcode":
                        col.data.append(faker.postcode())
                    elif col.clas == "automotive":
                        col.data.append(faker.license_plate())
                    elif col.clas == "iban":
                        col.data.append(faker.iban())
                    elif col.clas == "ean13":
                        col.data.append(faker.ean13())
                    elif col.clas == "ean8":
                        col.data.append(faker.ean8())
                    elif col.clas == "color":
                        col.data.append(faker.safe_color_name())
                    elif col.clas == "company":
                        col.data.append(faker.company())
                    elif col.clas == "credit_card_provider":
                        col.data.append(faker.credit_card_provider(card_type=None))
                    elif col.clas == "credit_card_full":
                        col.data.append(faker.credit_card_full(card_type=None))
                    elif col.clas == "currency_name":
                        col.data.append(faker.currency_name())
                    elif col.clas == "currency_code":
                        col.data.append(faker.currency_code())
                    elif col.clas == "date":
                        col.data.append(str(faker.date_this_year(before_today=True, after_today=True)))
                    elif col.clas == "timezone":
                        col.data.append(faker.timezone())
                    elif col.clas == "year":
                        col.data.append(faker.year())
                    elif col.clas == "date_time":
                        col.data.append(faker.iso8601(tzinfo=None, end_datetime=None))
                    elif col.clas == "mac_address":
                        col.data.append(faker.mac_address())
                    elif col.clas == "ipv4":
                        col.data.append(faker.ipv4_public())
                    elif col.clas == "url":
                        col.data.append(faker.url(schemes=None))
                    elif col.clas == "email":
                        col.data.append(faker.free_email())
                    elif col.clas == "decimal": 
                        col.data.append(faker.pydecimal(4,4,True))
                    elif col.clas == "string":
                        col.data.append(faker.pystr())
                    elif col.clas == "isbn10":
                        col.data.append(faker.isbn10(separator="-"))
                    elif col.clas == "isbn13":
                        col.data.append(faker.isbn13(separator="-"))
                    elif col.clas == "name" or col.clas == "":
                        col.data.append(faker.name())
                    elif col.clas == "first_name":
                        col.data.append(faker.first_name())
                    elif col.clas == "last_name":
                        col.data.append(faker.last_name())
                    elif col.clas == "phone_number":
                        col.data.append(formatPhoneNumber(faker.msisdn()))
                    elif col.clas == "number":
                        col.data.append(faker.pyint())
                    elif col.clas == "prefix":
                        col.data.append(faker.prefix())
                    elif col.clas == "title":
                        col.data.append(faker.suffix())
                    elif col.clas == "country":
                        col.data.append(faker.country())
                    elif col.clas == "city":
                        col.data.append(faker.city())
                    elif col.clas == "longid":
                        col.data.append(faker.itin())
                    else:
                        print("class not found for column: " + col.uname)
                        sys.exit()

            else:
                primarys = logicalModell.datenbank.getprimarycolumns(logicalModell.datenbank, logicalModell.datenbank.tablename(logicalModell.datenbank, col.reference))
                for primary in primarys:
                    if tabl.desc == "Created from <ent>":
                        if primary.uname == col.uname:
                            data = []
                            for dat in primary.data:
                                data.append(dat)
                            col.data = data
                    else:
                        if primary.uname == col.name:
                            data = []
                            for dat in primary.data:
                                data.append(dat)
                            col.data = data


def formatPhoneNumber(phone):
    formated = phone[:4] + "/" + phone[4:7] + "-" + phone[7:10] + "-" + phone[10:]
    return formated
