from  .models import LogisticWaiting
from django.db import connections
from collections import namedtuple

import pandas as pd
import numpy as np
from django_pandas.io import read_frame



def stock_checking(card):    
    with connections['ccs'].cursor() as cursor:
        cursor.execute('[ax-sqlrpt].daps.django.spDostepneZapasy @spKodPozycji=%s', [card])
        desc = cursor.description
        nt_results = namedtuple('Result', [col[0] for col in desc])
        procedure = [nt_results(*row) for row in cursor.fetchall()]
        stock = {}
        for parts in procedure:
            if parts.Magazyn == 'PMGP' or parts.Magazyn == 'PMGH' or parts.Magazyn == 'SMGS':
                if parts.Zarejestrowane > 0 or parts.FizycznieDostepne > 0:
                    stock.update({str(parts.KodPozycji) : int(parts.FizycznieDostepne) + int(parts.Zarejestrowane)})
        return stock
                
def all_pn_stock(queryset):
    parts = queryset
    unrepeated_pn = []
    for pn in parts:
        unrepeated_pn.append(pn.KodPozycji)
    stock = {}
    for part in unrepeated_pn:
        single_stock = stock_checking(part)
        if single_stock is not None:
            stock.update(single_stock)
    return stock

def parts_for_repair(repairs):
    repair_parts = {}
    for repair in repairs:
        repair_parts.update({ int(repair.NrNaprawy) :{ str(repair.KodPozycji) : int(repair.Ilosc) }})
    return repair_parts

def subset_repair_parts(set1, set2):
    return set1.issubset(set2)


def checking_enough_stock(stock, repairs):
    warehouse_stock = stock
    needed_stock = repairs
    repairs_to_releases = []    
    for repair, pnqty in needed_stock.items():
        set1 = set(pnqty.keys())
        set2 = set(warehouse_stock.keys())
        result = subset_repair_parts(set1, set2)
        if result == True:
            for part, qty in pnqty.items():
                if part in warehouse_stock.keys():                
                    remaining_stock = warehouse_stock.get(part) - qty
                    warehouse_stock.update({part: remaining_stock})
                    if int(warehouse_stock.get(part)) >= 0:
                        repairs_to_releases.append(repair)
                    elif int(warehouse_stock.get(part)) < 0:
                        set2.remove(part)                    
                    else:
                        continue
    return repairs_to_releases

    """for repair, pn_qty in repairs.items():
        for key, value in pn_qty.items():
            st = f'key:{key}, PN:{value}'"""
          