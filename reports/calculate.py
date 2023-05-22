from  .models import LogisticWaiting
from django.db import connections
from collections import namedtuple

import pandas as pd
import numpy as np
from django_pandas.io import read_frame


def unrepeated_pn_stock(queryset):
    parts = queryset
    unrepeated_pn = []
    for pn in parts:
        unrepeated_pn.append(pn.KodPozycji)
    return unrepeated_pn
    
def all_stock_checking(part):    
    with connections['ccs'].cursor() as cursor:
        cursor.execute('[ax-sqlrpt].daps.django.spDostepneZapasy @spKodPozycji=%s', [part])
        desc = cursor.description
        nt_results = namedtuple('Result', [col[0] for col in desc])
        procedure = [nt_results(*row) for row in cursor.fetchall()]
        stock_pmgp = {}
        stock_pmgh = {}
        stock_smgs = {}
        for parts in procedure:
            if parts.Magazyn == 'PMGP':
                if parts.Zarejestrowane > 0 or parts.FizycznieDostepne > 0:
                    stock_pmgp.update({str(parts.KodPozycji) : int(parts.FizycznieDostepne) + int(parts.Zarejestrowane)})
            if parts.Magazyn == 'PMGH':
                if parts.Zarejestrowane > 0 or parts.FizycznieDostepne > 0:
                    stock_pmgh.update({str(parts.KodPozycji) : int(parts.FizycznieDostepne) + int(parts.Zarejestrowane)})
            if parts.Magazyn == 'SMGS':
                if parts.Zarejestrowane > 0 or parts.FizycznieDostepne > 0:
                    stock_smgs.update({str(parts.KodPozycji) : int(parts.FizycznieDostepne) + int(parts.Zarejestrowane)})
    return stock_pmgp, stock_pmgh, stock_smgs

def all_pn_stock(unrepeated_pn):
    all_stock_pmgp = {}
    all_stock_pmgh = {}
    all_stock_smgs = {}
    for part in unrepeated_pn:
        stock_pmgp, stock_pmgh, stock_smgs = all_stock_checking(part)
        if stock_pmgp is not None:
            all_stock_pmgp.update(stock_pmgp)
        if stock_pmgh is not None:
            all_stock_pmgh.update(stock_pmgh)
        if stock_smgs is not None:
            all_stock_smgs.update(stock_smgs)
    return all_stock_pmgp, all_stock_pmgh, all_stock_smgs

def parts_for_repair(repairs):
    repair_parts = {}
    for repair in repairs:
        repair_parts.update({ int(repair.NrNaprawy) :{ str(repair.KodPozycji) : int(repair.Ilosc) }})
    return repair_parts

def subset_repair_parts(set1, set2):
    return set1.issubset(set2)


def checking_enough_stock(pmgp, pmgh, smgs, repairs, queryset):
    warehouse_stock = {}
    warehouse_stock.update(pmgp)
    warehouse_stock.update(pmgh)
    warehouse_stock.update(smgs)
    pmgp_warehouse = pmgp
    pmgh_warehouse = pmgh
    smgs_warehouse = smgs
    needed_stock = repairs
    repairs_to_releases = []
    payment_repair = []
    producers_included = ['ALCATEL', 'SAMSUNG', 'NOTHING', 'TCL', 'QLIVE']
    for rep in queryset:
        if rep.KodPozycjiTypNaprawy == "Płatna" and rep.Producent in producers_included:
            payment_repair.append(int(rep.NrNaprawy))  
    for repair, pnqty in needed_stock.items():
        set1 = set(pnqty.keys())
        set2 = set(warehouse_stock.keys())
        result = subset_repair_parts(set1, set2)
        if result == True:
            for part, qty in pnqty.items():
                if repair in payment_repair and part in pmgp_warehouse.keys():
                    continue
                elif part in pmgp_warehouse.keys():
                    remaining_pmgp_stock = pmgp_warehouse.get(part) - qty
                    pmgp_warehouse.update({part: remaining_pmgp_stock})
                    if int(pmgp_warehouse.get(part)) >= 0:
                        repairs_to_releases.append(repair)
                    elif int(pmgp_warehouse.get(part)) < 0:
                        set2.remove(part)                    
                    else:
                        continue
                elif part in pmgh_warehouse.keys():
                    remaining_pmgh_stock = pmgh_warehouse.get(part) - qty
                    pmgh_warehouse.update({part: remaining_pmgh_stock})
                    if int(pmgh_warehouse.get(part)) >= 0:
                        repairs_to_releases.append(repair)
                    elif int(pmgh_warehouse.get(part)) < 0:
                        set2.remove(part)                    
                    else:
                        continue
                elif part in smgs_warehouse.keys():
                    remaining_smgs_stock = smgs_warehouse.get(part) - qty
                    smgs_warehouse.update({part: remaining_smgs_stock})
                    if int(smgs_warehouse.get(part)) >= 0:
                        repairs_to_releases.append(repair)
                    elif int(smgs_warehouse.get(part)) < 0:
                        set2.remove(part)                    
                    else:
                        continue
                """if part in warehouse_stock.keys():                
                    remaining_stock = warehouse_stock.get(part) - qty
                    warehouse_stock.update({part: remaining_stock})
                    if int(warehouse_stock.get(part)) >= 0:
                        repairs_to_releases.append(repair)
                    elif int(warehouse_stock.get(part)) < 0:
                        set2.remove(part)                    
                    else:
                        continue"""
    return repairs_to_releases

    """for repair, pn_qty in repairs.items():
        for key, value in pn_qty.items():
            st = f'key:{key}, PN:{value}'"""
          