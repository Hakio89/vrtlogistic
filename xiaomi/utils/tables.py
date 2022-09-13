import pandas as pd
from django_pandas.io import read_frame


class Table:
    
    def __init__(self, delivery, parts=None, claim=None, waiting=None):
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
        
    def delivery_to_html(self):
        html = Table.read_delivery_file(self)
        return html.to_html(index=False, table_id="example2", classes="table table-striped table-bordered")
    
    def read_parts_file(self):
        """Read a parts file only"""
        parts = self.parts       
        
        if parts.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            parts = pd.read_excel(parts, 
                usecols=['Kod pozycji', 'Opis dla serwisu', 'Domyślny magazyn serwisu'],
                dtype={'Kod pozycji' : object, 'Opis dla serwisu' : object, 'Domyślny magazyn serwisu' : object})
            parts = parts.rename(columns={'Kod pozycji' : 'Parts Number',
                                    'Opis dla serwisu' : 'Parts Description PL',
                                    'Domyślny magazyn serwisu' : 'Warehouse'})        
            return parts
    
    def parts_to_html(self):
        html = Table.read_parts_file(self)
        return html.to_html(index=False, table_id="example3", classes="table table-striped table-bordered")
        
    def read_waiting_file(self):
        """Read a waiting file only"""
        waiting = self.waiting
        
        if waiting.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            waiting = pd.read_excel(waiting, 
                                      usecols=['Parts Number', 'Waiting'], 
                                      dtype={'Parts Number' : object, 'Waiting' : int})
        
            return waiting
    
    def waiting_to_html(self):
        html = Table.read_waiting_file(self)
        return html.to_html(index=False, table_id="example4", classes="table table-striped table-bordered")
        
    def read_claim_file(self):
        """Read a claim file only"""
        claim = self.claim
        
        claim = read_frame(claim, fieldnames=['claim_part', 'qty'])
        claim = claim.rename(columns={'claim_part' : 'Parts Number',
                                    'qty' : 'Claims'
                                    })
        return claim
    
    def claim_to_html(self):
        html = Table.read_claim_file(self)
        return html.to_html(index=False, table_id="example5", classes="table table-striped table-bordered")