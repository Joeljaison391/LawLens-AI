from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_invoice(company_name, branch_name, items, purchase_date, expiry_date, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, height - 40, "Fire Extinguisher Billing Invoice")
    
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 80, f"Company Name: {company_name}")
    c.drawString(40, height - 95, f"Branch Name: {branch_name}")
    c.drawString(40, height - 110, f"Purchase Date: {purchase_date}")
    c.drawString(40, height - 125, f"Expiry Date: {expiry_date}")
    
    c.drawString(40, height - 150, "Item Details:")
    c.line(40, height - 155, 550, height - 155)
    
    y_position = height - 170
    total_price = 0
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(40, y_position, "S.No")
    c.drawString(70, y_position, "Qty")
    c.drawString(110, y_position, "Description")
    c.drawString(230, y_position, "Type")
    c.drawString(330, y_position, "Unit Price")
    c.drawString(400, y_position, "Total Price")
    c.line(40, y_position - 5, 550, y_position - 5)
    
    c.setFont("Helvetica", 8)
    y_position -= 15
    serial_no = 1
    for item in items:
        qty, desc, size, unit_price = item
        total = qty * unit_price
        total_price += total
        
        c.drawString(40, y_position, str(serial_no))
        c.drawString(70, y_position, str(qty))
        c.drawString(110, y_position, desc)
        c.drawString(230, y_position, f"{size}")
        c.drawString(330, y_position, f"${unit_price:.2f}")
        c.drawString(400, y_position, f"${total:.2f}")
        
        y_position -= 15
        serial_no += 1
    
    c.line(40, y_position - 5, 550, y_position - 5)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(330, y_position - 20, "Grand Total:")
    c.drawString(400, y_position - 20, f"${total_price:.2f}")
    
    c.save()
    print(f"Invoice saved as {output_file}")

def get_user_input():
    company_name = input("Enter Company Name: ")
    branch_name = input("Enter Branch Name: ")
    purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")
    expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
    
    items = []
    serial_no = 1
    while True:
        print(f"\nEntering details for item {serial_no}:")
        qty = int(input("Enter Quantity: "))
        description = input("Enter Item Description: ")
        size = input("Enter Fire Extinguisher Type: ")
        unit_price = float(input("Enter Unit Price: "))
        items.append((qty, description, size, unit_price))
        serial_no += 1
        
        more_items = input("Do you want to add more items? (yes/no): ").strip().lower()
        if more_items != 'yes':
            break
    
    output_file = "fire_extinguisher_invoice.pdf"
    generate_invoice(company_name, branch_name, items, purchase_date, expiry_date, output_file)

if __name__ == "__main__":
    get_user_input()