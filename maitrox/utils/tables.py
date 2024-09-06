from django_pandas.io import read_frame

import pandas as pd


def open_delivery_file(file):
        """Read a delivery file only"""
        delivery = file        
        delivery = pd.read_excel(delivery,
                                usecols=['SO Number', 'Parts Number', 'Parts Desciption', 'Qty'])
        delivery = delivery.pivot_table(index=["SO Number", "Parts Number", "Parts Desciption"],
                                    values='Qty', aggfunc='sum')          
        delivery = delivery.reset_index()
        
        return delivery
    
def open_waitings_file(file):
        """Read a waitings file only"""
        waitings = file        
        waitings = pd.read_excel(waitings,
                                usecols=['Parts Number', 'Waiting'])
        waitings = waitings.pivot_table(index=["Parts Number", "Waiting"],
                                    values='Waiting', aggfunc='sum')          
        waitings = waitings.reset_index()
        
        return waitings
    
def open_parts_file(file):
        """Read a parts file only"""
        parts = file        
        parts = pd.read_excel(parts,
                                usecols=['Kod pozycji', 'Opis dla serwisu', 'Domyślny magazyn serwisu'])
        
        return parts

def read_ax_zz(queryset):
    query = read_frame(queryset, fieldnames=['ZamowienieZakupu', 'OdwolanieDoDostawcy', 'Status'])
    query = query.drop_duplicates()
    return query.to_html(index=False, classes='table mb-0 table-dark table-striped')

class Table:
    
    def __init__(self, delivery=None, parts=None, claim=None, waiting=None):
        self.delivery = delivery
        self.parts = parts
        self.claim = claim
        self.waiting = waiting 
        
    def __iter__(self):
        return self       
        
    def read_delivery_file(self):
        """Read a delivery file only"""
        delivery = self.delivery.file
        
        if delivery.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            delivery = pd.read_excel(delivery,
                                usecols=['SO Number', 'Parts Number', 'Parts Desciption', 'Qty'], 
                                dtype={'SO Number' : object, 'Parts Number' : object, 'Parts Desciption' : object, 'Qty' : int})
            
            delivery = delivery.pivot_table(index=["SO Number", "Parts Number", "Parts Desciption"],
                                    values='Qty', aggfunc='sum')            
            delivery = delivery.reset_index()
            return delivery
    
    def read_parts_file(self):
        """Read a parts file only"""
        parts = self.parts.file    
        
        if parts.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            parts = pd.read_excel(parts, 
                usecols=['Kod pozycji', 'Opis dla serwisu', 'Domyślny magazyn serwisu'],
                dtype={'Kod pozycji' : object, 'Opis dla serwisu' : object, 'Domyślny magazyn serwisu' : object})
            parts = parts.rename(columns={'Kod pozycji' : 'Parts Number',
                                    'Opis dla serwisu' : 'Parts Desciption PL',
                                    'Domyślny magazyn serwisu' : 'Warehouse'})      
            return parts
        
    def parts_to_html(self):
        parts = self.read_parts_file()
        return parts.to_html(index=False, table_id="example2", classes="table table-striped table-bordered") 
    
    def read_waiting_file(self):
        """Read a waiting file only"""
        waiting = self.waiting.file
        
        if waiting.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            waiting = pd.read_excel(waiting, 
                                      usecols=['Parts Number', 'Waiting'], 
                                      dtype={'Parts Number' : object, 'Waiting' : int})
            waiting = waiting.pivot_table(index=["Parts Number"],
                                    values='Waiting', aggfunc='sum')
            waiting = waiting.reset_index()
            return waiting
        
    def waiting_to_html(self):
        waiting = self.read_waiting_file()
        return waiting.to_html(index=False, table_id="example2", classes="table table-striped table-bordered") 
    
    def read_claim_file(self):
        """Read a claim file only"""
        claim = self.claim        
        claim = read_frame(claim, fieldnames=['claim_part', 'qty', 'status'])
        claim = claim.rename(columns={'claim_part' : 'Parts Number',
                                    'qty' : 'Claims',
                                    'status' : 'Claim Status',
                                    })
        #filter
        waiting_claim = claim['Claim Status'] == "Waiting"
        
        claim = claim[waiting_claim]
        claim = claim.pivot_table(index=["Parts Number"],
                                    values='Claims', aggfunc='sum')            
        claim = claim.reset_index()        
        return claim
  
    def delivery_joining(self):
        """Open files needed to be joined and join them in one delivery. Parts which has no descriptions are displays as Lack of Parts"""
        delivery = self.read_delivery_file()
        parts = self.read_parts_file()
        waiting = self.read_waiting_file()
        claim = self.read_claim_file()
        
        delivery = delivery.set_index('Parts Number')
        if parts.empty == False:
            delivery = delivery.join(parts.set_index('Parts Number'))
        if claim.empty == False:
            delivery = delivery.join(claim.set_index('Parts Number'))
        if waiting.empty == False:
            delivery = delivery.join(waiting.set_index('Parts Number'))
        
        delivery = delivery.reset_index()
        delivery = delivery.fillna(int(0))   
        
        if waiting.empty == False:
            delivery['Waiting'] = delivery['Waiting'].astype(dtype=int)
        if claim.empty == False:
            delivery['Claims'] = delivery['Claims'].astype(dtype=int)
        delivery['Parts Number'] = delivery['Parts Number'].astype(dtype=str)
        delivery['Parts Desciption'] = delivery['Parts Desciption'].astype(dtype=str)
        delivery['Qty'] = delivery['Qty'].astype(dtype=int)
        if parts.empty == False:
            delivery['Parts Desciption PL'] = delivery['Parts Desciption PL'].astype(dtype=str).str.replace('\n', '') 
            delivery['Warehouse'] = delivery['Warehouse'].astype(dtype=str)
        return delivery
    
    def pmgp_delivery(self, del_data):
        """Returns data for PMGP warehouse only"""
        delivery = del_data        
        warehouse_pmgp = delivery['Warehouse'] == 'PMGP'
        pmgp = delivery[warehouse_pmgp]
        return pmgp
    
    def pmgh_delivery(self, del_data):
        """Returns data for PMGH warehouse only"""
        delivery = del_data        
        warehouse_pmgh = delivery['Warehouse'] == 'PMGH'
        pmgh = delivery[warehouse_pmgh] 
        return pmgh
    
    def nan_delivery(self, del_data):
        """Returns data for parts which are not included in PMGP and PMGH warehouse"""
        delivery = del_data        
        warehouse_pmgp_nan = delivery['Warehouse'] != 'PMGP'
        warehouse_pmgh_nan = delivery['Warehouse'] != 'PMGH'
        warehouse_nan = warehouse_pmgp_nan & warehouse_pmgh_nan
        return delivery[warehouse_nan]
    
    
            
    def read_base(self):
        """Returns data as a dataframe from datatbase"""
        file = self.delivery
        data_base = read_frame(file, fieldnames=['delivery', 'status'], )
        data_base = data_base.rename(columns={
            'delivery': 'Numer SO',
            'status': 'Status',
        })
        data_base = data_base.set_index('Numer SO')        
        return data_base
        
    def __next__(self):
        """Generator that creates data to be included in email message"""
        all_deliveries = self.delivery        
    
        for delivery in all_deliveries:
            if delivery.status.status != "Transport":
                continue 
            else:
                   
                delivery_instance = Table(delivery=delivery)
                current_delivery = delivery_instance.read_delivery_file()
                parts = self.read_parts_file()            
                waiting = self.read_waiting_file()
                deliveries = current_delivery.set_index('Parts Number')
                deliveries = deliveries.join([
                    parts.set_index('Parts Number'), 
                    waiting.set_index('Parts Number')], lsuffix="", rsuffix="")
                
                deliveries = deliveries.reset_index()
                deliveries = deliveries.fillna(int(0))
                
                mail_detail = deliveries.pivot_table(
                    index=["SO Number"],
                    values=['Qty', 'Waiting'],
                    aggfunc='sum')                
                mail_detail = mail_detail.reset_index()
                mail_detail = mail_detail.rename(
                    columns={
                        'SO Number' : 'Numer SO',
                        'Qty' : 'Ilość',
                        'Waiting' : 'CZEKA'
                    })
                
                mail_detail = mail_detail.set_index('Numer SO')
                
                
                warehouse_pmgp = deliveries['Warehouse'] == 'PMGP'
                warehouse_pmgh = deliveries['Warehouse'] == 'PMGH'
                warehouse_pmgp_nan = deliveries['Warehouse'] != 'PMGP'
                warehouse_pmgh_nan = deliveries['Warehouse'] != 'PMGH'
                warehouse_nan = warehouse_pmgp_nan & warehouse_pmgh_nan
                
                pmgp = deliveries[warehouse_pmgp]
                pmgh = deliveries[warehouse_pmgh]
                nan = deliveries[warehouse_nan]
                
                mail_detail['PMGP QTY'] = int(pmgp['Qty'].sum())
                mail_detail['PMGP PN'] = int(len(pmgp['Qty']))
                mail_detail['PMGH QTY'] = int(pmgh['Qty'].sum())
                mail_detail['PMGH PN'] = int(len(pmgh['Qty']))
                mail_detail['Ilość'] = int(pmgp['Qty'].sum()) +  int(pmgh['Qty'].sum()) + int(nan['Qty'].sum())
                mail_detail['CZEKA PMGP'] = int(pmgp['Waiting'].sum())
                mail_detail['CZEKA PMGH'] = int(pmgh['Waiting'].sum())
                mail_detail['CZEKA'] = int(pmgh['Waiting'].sum()) + int(pmgp['Waiting'].sum())
                mail_detail['Nowe PN'] = int(len(nan['Qty']))
                
                
                data_base = self.read_base()
                mail_detail = mail_detail.join(data_base)
                mail_detail = mail_detail.reset_index()
                yield mail_detail
        
    #Connect all needed tables to mail report and adds sumup
    def mail_report(self):
        """Creates email report"""
        mail_detail = self.__next__()
        report = pd.concat(mail_detail, axis=0)
        sumdel = report['Ilość'].sum()
        sump = report['PMGP QTY'].sum()
        sumkp = report['PMGP PN'].sum()
        sumh = report['PMGH QTY'].sum()
        sumkh = report['PMGH PN'].sum()
        sumnk = report['Nowe PN'].sum()
        sumcp = int(report['CZEKA PMGP'].sum())
        sumch = int(report['CZEKA PMGH'].sum())
        sumcs = sumcp + sumch
        
        sumup = {
            'Numer SO' : str(''),
            'Ilość' : sumdel,
            'CZEKA' : sumcs,
            'PMGP QTY' : sump,
            'PMGP PN' : sumkp,
            'PMGH QTY' : sumh,
            'PMGH PN' : sumkh,
            'Nowe PN' : sumnk,
            'CZEKA PMGP' : sumcp,
            'CZEKA PMGH' : sumch,
            'Status' : str(''),
        }

        report = report.fillna(str(""))
        report = report.to_html(index=False, table_id="customers")   
        return report