from django_pandas.io import read_frame

import pandas as pd
from datetime import datetime

class Table:
    
    def __init__(self, delivery=None, parts=None, claim=None, waiting=None):
        self.delivery = delivery
        self.parts = parts
        self.claim = claim
        self.waiting = waiting        
        
    def read_delivery_file(self):
        """Read a delivery file only"""
        delivery = self.delivery
        
        if delivery.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            delivery = pd.read_excel(delivery,
                                usecols=['SO Number', 'Parts Number', 'Parts Desciption', 'Qty'], 
                                dtype={'SO Number' : object, 'Parts Number' : object, 'Parts Desciption' : object, 'Qty' : int})
            
            delivery = delivery.pivot_table(index=["Parts Number", "Parts Desciption"],
                                    values='Qty', aggfunc='sum')            
            delivery = delivery.reset_index()
            return delivery
    
    def read_parts_file(self):
        """Read a parts file only"""
        parts = self.parts       
        
        if parts.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            parts = pd.read_excel(parts, 
                usecols=['Kod pozycji', 'Opis dla serwisu', 'Domyślny magazyn serwisu'],
                dtype={'Kod pozycji' : object, 'Opis dla serwisu' : object, 'Domyślny magazyn serwisu' : object})
            parts = parts.rename(columns={'Kod pozycji' : 'Parts Number',
                                    'Opis dla serwisu' : 'Parts Desciption PL',
                                    'Domyślny magazyn serwisu' : 'Warehouse'})      
            return parts
    
    def parts_to_html(self):
        
        html = self.read_parts_file()
        return html.to_html(index=False, table_id="example2", classes="table table-striped table-bordered")
        
    def read_waiting_file(self):
        """Read a waiting file only"""
        waiting = self.waiting
        
        if waiting.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            waiting = pd.read_excel(waiting, 
                                      usecols=['Parts Number', 'Waiting'], 
                                      dtype={'Parts Number' : object, 'Waiting' : int})
            waiting = waiting.pivot_table(index=["Parts Number"],
                                    values='Waiting', aggfunc='sum')
            waiting = waiting.reset_index()
            return waiting
    
    def waiting_to_html(self):
        html = self.read_waiting_file()
        return html.to_html(index=False, table_id="example2", classes="table table-striped table-bordered")
        
    def read_claim_file(self):
        """Read a claim file only"""
        claim = self.claim
        
        claim = read_frame(claim, fieldnames=['claim_part', 'qty'])
        claim = claim.rename(columns={'claim_part' : 'Parts Number',
                                    'qty' : 'Claims'
                                    })
        return claim
    
    def claim_to_html(self):
        html = self.read_claim_file()
        return html.to_html(index=False, table_id="example2", classes="table table-striped table-bordered")
    
    def delivery_joining(self):
        """Opens file needed to be joined and join then in one delivery. Pars which has no descriptions are displays as Lack of Parts"""
        delivery = self.read_delivery_file()
        parts = self.read_parts_file()
        waiting = self.read_waiting_file()
        claim = self.read_claim_file()
        
        delivery = delivery.set_index('Parts Number')
        
        delivery = delivery.join([
            parts.set_index('Parts Number'), 
            claim.set_index('Parts Number'), 
            waiting.set_index('Parts Number')], lsuffix="", rsuffix="")
        
        delivery = delivery.reset_index()
        delivery = delivery.fillna(int(0))        
        
        delivery['Waiting'] = delivery['Waiting'].astype(dtype=int)
        delivery['Claims'] = delivery['Claims'].astype(dtype=int)
        delivery['Parts Number'] = delivery['Parts Number'].astype(dtype=str)
        delivery['Parts Desciption'] = delivery['Parts Desciption'].astype(dtype=str)
        delivery['Qty'] = delivery['Qty'].astype(dtype=int)
        delivery['Parts Desciption PL'] = delivery['Parts Desciption PL'].astype(dtype=str)
        delivery['Warehouse'] = delivery['Warehouse'].astype(dtype=str)
        
        warehouse_pmgp = delivery['Warehouse'] == 'PMGP'
        pmgp = delivery[warehouse_pmgp]
        warehouse_pmgh = delivery['Warehouse'] == 'PMGH'
        pmgh = delivery[warehouse_pmgh]     
        warehouse_pmgp_nan = delivery['Warehouse'] != 'PMGP'
        warehouse_pmgh_nan = delivery['Warehouse'] != 'PMGH'
        warehouse_nan = warehouse_pmgp_nan & warehouse_pmgh_nan
        
        del_empty = delivery[warehouse_nan].empty
        
        pmgp_len = len(pmgp)
        pmgh_len = len(pmgh)
        
        pmgp_sum = pmgp['Qty'].sum()
        pmgh_sum = pmgp['Qty'].sum()
        
        pmgp_html = pmgp.to_html(index=False, table_id="example2", classes="table table-striped table-bordered")
        pmgh_html = pmgh.to_html(index=False, table_id="example3", classes="table table-striped table-bordered")
        del_nan = delivery[warehouse_nan].to_html(index=False, table_id="example4", classes="table table-striped table-bordered")
        return pmgp_len, pmgh_len, pmgp_sum, pmgh_sum, pmgp_html, pmgh_html, del_nan, del_empty
            
        

       