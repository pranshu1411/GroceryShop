function showInput(option) {
    document.getElementById('inputBoxContainer').style.display = 'block';
    document.getElementById('selectedOption').value = option;
}

function fetchRecord(admin) {
    let option = document.getElementById('selectedOption').value;
    let recordID = document.getElementById('recordID').value;

    fetch('/fetch_record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({admin: admin, option: option, recordID: recordID })
    })
        .then(response => response.json())
        .then(data => {
            if (data === null) {
                document.getElementById('updateFormContainer').style.display = 'none';
                let alertDiv = document.getElementById('flashedMessage');
                alertDiv.innerHTML = `<div class="container">
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <span>No record found with this ID</span>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>`;
            }
            else{
                populateForm(data, option);
            }
        })
        .catch(error => console.error('Error:', error));
}

function populateForm(data, option) {
    document.getElementById('updateFormContainer').style.display = 'block';
    if (option == 'inventory') {
        document.getElementById('updateForm').innerHTML =
            `<div id="inventoryForm" style="margin-left: 50px; margin-top: 30px; margin-right: 100px;">
                <div class="row">
                <input type = "hidden" id = "primarykey" name = "primarykey" value = "${data.itemID}">
                    <div class="col-6">
                        <label for="itemName">Name:</label><br>
                        <input type="text" id="itemName" name="itemName" maxlength="50" value="${data.ItemName}" required readonly><br><br>
                    </div>
                    <div class="col-6">
                        <label for="category">Category:</label><br>
                        <input type="text" id="category" name="category" maxlength="50" value="${data.category}" required readonly><br><br>
                    </div>
                </div>
    
                <div class="row">
                    <div class="col-4">
                        <label for="price">Price:</label><br>
                        <input type="number" id="price" name="price" min="0" value="${data.price}" required readonly><br><br>
                    </div>
                    <div class="col-4">
                        <label for="unit">Unit:</label><br>
                        <input type="text" id="unit" name="unit" maxlength="50" value="${data.Unit}" required readonly><br><br>
                    </div>
                    <div class="col-4">
                        <label for="stock">Stock:</label><br>
                        <input type="number" id="stock" name="stock" min="0" value="${data.stock}" required readonly><br><br>
                    </div>
                </div>
    
                <div style="width: 1000px;">
                    <label for="itemDescription">Item Description:</label><br>
                    <textarea id="itemDescription" name="itemDescription" maxlength="100" required readonly>${data.itemDescription}</textarea><br><br>
                </div>
    
                <div class="d-grid gap-2 col-6 mx-auto">
                    <button class="btn btn-dark" type="submit" name="submit_method" value="inventory" style="font-size: 20px; margin-bottom: 20px;">Delete From Inventory</button>
                </div>
        </div>`;
    }
    else if (option == 'supplier') {
        document.getElementById('updateForm').innerHTML =
            `<div id="suppliersForm" style="margin-left: 50px; margin-top: 30px; margin-right: 100px;">
                <div class="row">
                <input type = "hidden" id = "primarykey" name = "primarykey" value = "${data.Supplier_ID}">
                    <div class="col-6">
                        <label for="supplierName">Supplier Name:</label><br>
                        <input type="text" id="supplierName" name="supplierName" maxlength="50" value="${data.Name}" required readonly><br><br>
                    </div>
                    <div class="col-6">
                        <label for="category">Category:</label><br>
                        <input type="text" id="category" name="category" maxlength="50" value="${data.Category}" required readonly><br><br>
                    </div>
                </div>
    
                <div class="row">
                    <div class="col-12">
                        <label for="AddressLine1">Address Line 1:</label><br>
                        <input type="text" id="AddressLine1" name="AddressLine1" maxlength="100" value="${data.AddressLine1}" required readonly><br><br>
                    </div>
                </div>
    
                <div class="row">
                    <div class="col-12">
                        <label for="AddressLine2">Address Line 2:</label><br>
                        <input type="text" id="AddressLine2" name="AddressLine2" maxlength="100" value="${data.AddressLine2}" required readonly><br><br>
                    </div>
                </div>
    
                <div class="row">
                    <div class="col-3">
                        <label for="city">City:</label><br>
                        <input type="text" id="city" name="city" maxlength="100" value="${data.City}" required readonly><br><br>
                    </div>
                    <div class="col-3">
                        <label for="state">State:</label><br>
                        <input type="text" id="state" name="state" maxlength="100" value="${data.State}" required readonly><br><br>
                    </div>
                    <div class="col-3">
                        <label for="country">Country:</label><br>
                        <input type="text" id="country" name="country" maxlength="100" value="${data.Country}" required readonly><br><br>
                    </div>
                    <div class="col-3">
                        <label for="pincode">Pin code:</label><br>
                        <input type="number" id="pincode" name="pincode" min="100000" max="999999" value="${data.PIN_code}" required readonly><br><br>
                    </div>
                </div>
    
                <div class="d-grid gap-2 col-6 mx-auto">
                    <button class="btn btn-dark" type="submit" name="submit_method" value="supplier"
                        style="font-size: 20px; margin-bottom: 20px;">Delete Supplier</button>
                </div>
        </div>`;
    }
    else if (option == 'delivery') {
        document.getElementById('updateForm').innerHTML =
        `<div id="deliveryForm" style="margin-left: 50px; margin-top: 30px; margin-right: 100px;">
            <div class="row">
            <input type = "hidden" id = "primarykey" name = "primarykey" value = "${data.AgentID}">
                <div class="col-12">
                    <label for="agentname">Agent Name:</label><br>
                    <input type="text" id="agentname" name="agentname" maxlength="100" value="${data.AgentName}" required readonly><br><br>
                </div>
            </div>

            <div class="row">
                <div class="col-12">
                    <label for="phonenumber">Phone number:</label><br>
                    <input type="number" id="phonenumber" name="phonenumber" min="1000000000" max="9999999999" value="${data.PhoneNumber}" required readonly><br><br>
                </div>
            </div>

            <div class="d-grid gap-2 col-6 mx-auto">
                <button class="btn btn-dark" type="submit" name="submit_method" value="delivery"
                    style="font-size: 20px; margin-bottom: 20px;">Delete Delivery Agent</button>
            </div>
    </div>`
    }
}