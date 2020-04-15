import datetime
from openpyxl import Workbook
from openpyxl import styles
from src.common.utils1 import Utils
from src.common.database import Database
from src.models.invoices.invoice import Invoice
from src.models.invoices.invoice_item import Invoice_item
from src.models.invoices.serial_no import Serial_no
from src.models.items.item import Item
from src.models.parties.party import Party


class Excel_export(object):
    def __init__(self,start,end):
        self.start = datetime.datetime.strptime(start,'%d-%m-%Y')
        self.end = datetime.datetime.strptime(end,'%d-%m-%Y')
        self.gst = []
        self.igst =[]

    def make_final_workbook(self):
        gst=[]
        igst = []
        gst.append(['Date','Number','Party Name','City','GSTIN','Product Model Name','Quantity','Rate Per','Base Price','SGST','CGST','Total','Serial_No','e-Way Bill No.'])
        igst.append(['Date', 'Number', 'Party Name', 'City', 'GSTIN', 'Product Model Name', 'Quantity', 'Rate Per',
                    'Base Price', 'IGST', 'Total', 'Serial_No','e-Way Bill No.'])
        gst.append([])
        igst.append([])
        invoices = Invoice.filter_by_date(self.start,self.end)
        print(invoices)

        for invoice in invoices:
            total_invoice,total_base_price,total_tax = 0,0,0
            invoice.date = datetime.datetime.strftime(invoice.date,'%d-%m-%Y')
            invoice.party_id = Party.get_by_id(invoice.party_id)
            invoice_items = Invoice_item.get_by_invoice_id(invoice._id)
            flag = False
            if invoice.party_id.tax_type() == 'gst':
                flag = True
            for invoice_item in invoice_items:

                invoice_item.item_id = Item.get_by_id(invoice_item.item_id)
                y = []
                serial_nos = Serial_no.get_by_invoice_item_id(invoice_item._id)
                q=''
                for i in serial_nos:
                    q = q+i.serial_no+'\n'
                print(q)
                invoice_item.quantity = int(invoice_item.quantity)
                invoice_item.rate_per = float(invoice_item.rate_per)
                invoice_item.item_id.tax = float(invoice_item.item_id.tax)
                base_price = invoice_item.rate_per * invoice_item.quantity
                tax = (base_price * invoice_item.item_id.tax) / 100
                total = base_price + tax
                total_base_price +=base_price
                total_tax +=tax
                total_invoice+=total
                if flag:
                    y = [invoice.date,
                         invoice.no,
                         invoice.party_id.name,
                         invoice.party_id.city,
                         invoice.party_id.gstin,
                         invoice_item.item_id.model_name,
                         invoice_item.quantity,
                         invoice_item.rate_per,
                         base_price,
                         tax/2,
                         tax/2,
                         total,
                         q]
                    gst.append(y)
                else:
                    y = [invoice.date,
                         invoice.no,
                         invoice.party_id.name,
                         invoice.party_id.city,
                         invoice.party_id.gstin,
                         invoice_item.item_id.model_name,
                         invoice_item.quantity,
                         invoice_item.rate_per,
                         base_price,
                         tax,
                         total,
                         q]
                    igst.append(y)
            if flag:
                gst.append(['','','','','','','','','',total_base_price,total_tax/2,total_tax/2,total_invoice,invoice.e_way])
                gst.append([])
            else:
                igst.append(['','','','','','','','','',total_base_price,total_tax,total_invoice,invoice.e_way])
                igst.append([])
        print(igst)
        print(gst)
        for i in igst:
            print(i)
        print()
        for i in gst:
            print(i)
        self.gst = gst
        self.igst = igst
        self.make_workbook(gst,igst)

    def make_workbook(self,gst,igst):
        len_gst = len(gst)
        len_igst = len(igst)
        wb = Workbook()
        x=datetime.datetime.strftime(self.start,'%d-%m-%Y')

        y=datetime.datetime.strftime(self.end,'%d-%m-%Y')
        c = Utils.current_time()
        c = datetime.datetime.strftime(c,'%d-%m-%Y')
        dest_filename = c+'_'+x+'_'+y+'_'+str(len_igst+len_gst)+'.xlsx'

        ws1 = wb.active
        ws1.title = "GST"

        for row in range(len_gst):
            ws1.append(gst[row])
            ws1['M'+str(row+1)].alignment = styles.Alignment(wrap_text=True)

        wb["GST"].freeze_panes = "A2"

        ws2=wb.create_sheet('IGST')

        for row in range(len_igst):
            ws2.append(igst[row])
            ws2['L'+str(row+1)].alignment = styles.Alignment(wrap_text=True)
        wb["IGST"].freeze_panes = "A2"

        wb.save("C:\\Users\\Dell\\Desktop\\"+dest_filename)


#Database.initialize()
#start = datetime.datetime.strptime('27-01-2019','%d-%m-%Y')
#end = datetime.datetime.strptime('27-08-2019','%d-%m-%Y')
#x = Excel_export(start,end).make_sheet()
#print(x.gst)
#print(x.igst)