function showForm(formType) {
    document.getElementById('inventoryForm').style.display = 'none';
    document.getElementById('suppliersForm').style.display = 'none';
    document.getElementById('deliveryForm').style.display = 'none';

    if (formType === 'inventory') {
        document.getElementById('inventoryForm').style.display = 'block';
    } else if (formType === 'suppliers') {
        document.getElementById('suppliersForm').style.display = 'block';
    } else if (formType === 'delivery') {
        document.getElementById('deliveryForm').style.display = 'block';
    }
}
