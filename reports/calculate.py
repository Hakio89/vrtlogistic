from  .models import LogisticWaiting
from django.db import connections
from collections import namedtuple

import pandas as pd
import numpy as np
from django_pandas.io import read_frame


def unrepeated_pn_stock(queryset):
    """Verifying all part numbers in queryset and returning a list of individual PN numbers
    
    Args:
        queryset(queryset): needs a queryset to ve given

    Returns:
        list: list of individual PN numbers
    """   
    parts = queryset
    unrepeated_pn = []
    for pn in parts:
        if pn.KodPozycji in unrepeated_pn:
            continue
        else:
            unrepeated_pn.append(pn.KodPozycji)
    return unrepeated_pn
    
def all_stock_checking(part):
    """Function sends query with a specified part number and receives specific stock
    for the given part.

    Args:
        part (str): needs part number as a string

    Returns:
        dict: returns dictionaries of PMGP, PMGH, SMSGS, Tech PMGP and Tech SMGS stock.
    """
    with connections['ccs'].cursor() as cursor:
        cursor.execute('[ax-sqlrpt].daps.django.spDostepneZapasy @spKodPozycji=%s', [part])
        desc = cursor.description
        nt_results = namedtuple('Result', [col[0] for col in desc])
        procedure = [nt_results(*row) for row in cursor.fetchall()]
        stock_pmgp = {}
        stock_pmgh = {}
        stock_smgs = {}
        tech_stock_pmgp = {}
        tech_stock_smgs = {}
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
            if str(parts.Magazyn).startswith('GP') and parts.Lokalizacja == "SPRAWNE":
                if parts.Zarejestrowane > 0 or parts.FizycznieDostepne > 0:
                    if str(parts.KodPozycji) in tech_stock_pmgp:
                        new_qty = int(tech_stock_pmgp.get(str(parts.KodPozycji))) + int(parts.FizycznieDostepne)
                        tech_stock_pmgp.update({str(parts.KodPozycji) : new_qty})
                    else:
                        tech_stock_pmgp.update({str(parts.KodPozycji) : int(parts.FizycznieDostepne)})
            if str(parts.Magazyn).startswith('GS') and parts.Lokalizacja == "SPRAWNE":
                if parts.Zarejestrowane > 0 or parts.FizycznieDostepne > 0:
                    if str(parts.KodPozycji) in tech_stock_smgs:
                        new_qty = int(tech_stock_smgs.get(str(parts.KodPozycji))) + int(parts.FizycznieDostepne)
                        tech_stock_smgs.update({str(parts.KodPozycji) : new_qty})
                    else:
                        tech_stock_smgs.update({str(parts.KodPozycji) : int(parts.FizycznieDostepne)})
    return stock_pmgp, stock_pmgh, stock_smgs, tech_stock_pmgp, tech_stock_smgs

def all_pn_stock(unrepeated_pn):
    """Function i using function all_stock_checking to help with creating stock for all parts
    in from the specified list of parts.

    Args:
        unrepeated_pn (list): List of parts to create a certain stock.

    Returns:
        dict: returns dict of stocks devided by specific warehouse: PMGP, PMGH, SMSG, Tech PMGP and Tech SMGS
    """
    all_pmgp = {}
    all_pmgh = {}
    all_smgs = {}
    all_tech_pmgp = {}
    all_tech_smgs = {}
    for part in unrepeated_pn:
        stock_pmgp, stock_pmgh, stock_smgs, tech_stock_pmgp, tech_stock_smgs = all_stock_checking(part)
        if stock_pmgp is not None:
            all_pmgp.update(stock_pmgp)
        if stock_pmgh is not None:
            all_pmgh.update(stock_pmgh)
        if stock_smgs is not None:
            all_smgs.update(stock_smgs)
        if tech_stock_pmgp is not None:
            all_tech_pmgp.update(tech_stock_pmgp)
        if tech_stock_smgs is not None:
            all_tech_smgs.update(tech_stock_smgs)
    return all_pmgp, all_pmgh, all_smgs, all_tech_pmgp, all_tech_smgs

def parts_for_repair(repairs):
    """Showing the dict of all waiting repairs with parts and their quantities 
    needed to close specific repair.

    Args:
        repairs (queryset): set queryset to be checked

    Returns:
        dict: returns a dictionary of all repairs with parts and their qty
    """
    repair_parts = {}
    set_repair_parts = {}
    for repair in repairs:
        if int(repair.NrNaprawy) in set_repair_parts.keys():
            values = set_repair_parts.get(int(repair.NrNaprawy))          
            values.append(str(repair.KodPozycji))
            set_repair_parts.update({ int(repair.NrNaprawy): values})
        else:
            set_repair_parts.update({ int(repair.NrNaprawy): [str(repair.KodPozycji)]})
        repair_parts.update({ int(repair.NrNaprawy): { str(repair.KodPozycji): int(repair.Ilosc) }})
    return repair_parts, set_repair_parts

def subset_repair_parts(set1, set2):
    """Checking two sets if one of them  is a subset of another

    Args:
        set1 (set): firts set to compare
        set2 (set): second set to compare

    Returns:
        bool: return True or False
    """
    return set1.issubset(set2)


def checking_enough_stock(
        pmgp, pmgh, smgs, tech_pmgp, tech_smgs, repairs, set_repair, queryset
        ):
    warehouse_stock = {}
    warehouse_stock.update(pmgp)
    warehouse_stock.update(pmgh)
    warehouse_stock.update(smgs)
    pmgp_warehouse = pmgp
    pmgh_warehouse = pmgh
    smgs_warehouse = smgs
    pmgp_tech = tech_pmgp
    smgs_tech = tech_smgs
    needed_stock = repairs
    set_repair_parts = set_repair
    repairs_to_releases = []
    payment_repair = []
    producers_included = ['ALCATEL', 'SAMSUNG', 'NOTHING', 'TCL', 'QLIVE']
    for rep in queryset:
        if rep.KodPozycjiTypNaprawy == "Płatna" and rep.Producent in producers_included:
            if int(rep.NrNaprawy) not in payment_repair:
                payment_repair.append(int(rep.NrNaprawy))
            else:
                continue
    for repair, pnqty in needed_stock.items():
        if repair in set_repair_parts.keys():
            set1 = set(set_repair_parts.get(repair))
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
                        elif part in pmgp_tech.keys():
                            remaining_pmgp_stock = pmgp_tech.get(part) - qty
                            pmgp_tech.update({part: remaining_pmgp_stock})
                            if int(pmgp_tech.get(part)) >= 0:
                                repairs_to_releases.append(repair)
                            elif int(pmgp_warehouse.get(part)) < 0 and int(pmgp_tech.get(part)) < 0:
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
                        elif part in smgs_tech.keys():
                            remaining_smgs_stock = smgs_tech.get(part) - qty
                            smgs_tech.update({part: remaining_smgs_stock})
                            if int(smgs_tech.get(part)) >= 0:
                                repairs_to_releases.append(repair)
                            elif int(smgs_warehouse.get(part)) < 0 and int(smgs_tech.get(part)) < 0:
                                set2.remove(part)                    
                            else:
                                continue
    return repairs_to_releases