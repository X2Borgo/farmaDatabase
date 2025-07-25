function renderCreatePrescriptionPage() {
    const content = document.getElementById('content');
    
    // Check role permission
    const userToken = localStorage.getItem('token');
    if (!userToken) {
        navigateTo('login');
        return;
    }
    
    const userData = JSON.parse(userToken);
    if (userData.role !== 'practitioner') {
        content.innerHTML = `
            <div class="card">
                <h2>Access Denied</h2>
                <p>Only general practitioners can create prescriptions.</p>
                <button class="btn" onclick="navigateTo('home')">Back to Home</button>
            </div>
        `;
        return;
    }
    
    // Display the prescription form for practitioners
    content.innerHTML = `
        <div class="card">
            <h2>Create New Prescription</h2>
            
            <form id="prescription-form">
                <div class="form-group">
                    <label for="patient-name">Patient Name</label>
                    <input type="text" id="patient-name" name="patientName" required>
                </div>
                
                <div class="form-group">
                    <label for="prescription-type">Prescription Type</label>
                    <select id="prescription-type" name="prescriptionType" required>
                        <option value="">-- Select Type --</option>
                        <option value="regular">Regular</option>
                        <option value="controlled">Controlled Substance</option>
                        <option value="recurring">Recurring</option>
                    </select>
                </div>
                
                <div id="medications-section">
                    <h3>Medications</h3>
                    <div id="medications-list">Loading available medications...</div>
                    <div id="prescription-items">
                        <p>No medications added to prescription</p>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="prescription-notes">Notes & Instructions</label>
                    <textarea id="prescription-notes" name="notes" rows="3"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="valid-until">Valid Until</label>
                    <input type="date" id="valid-until" name="validUntil" required>
                </div>
                
                <button type="submit" class="btn btn-primary">Create Prescription</button>
                <button type="button" class="btn" onclick="navigateTo('home')">Cancel</button>
            </form>
        </div>
    `;
    
    // Set today as minimum date for validity
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    document.getElementById('valid-until').min = formattedDate;
    
    // Default validity to 30 days from now
    const defaultDate = new Date();
    defaultDate.setDate(defaultDate.getDate() + 30);
    document.getElementById('valid-until').value = defaultDate.toISOString().split('T')[0];
    
    // Load available medications
    loadMedicationsForPrescription();
    
    // Set up form handler
    const form = document.getElementById('prescription-form');
    form.addEventListener('submit', handlePrescriptionSubmit);
}

// Global variable to track prescription items
const prescriptionItems = [];

async function loadMedicationsForPrescription() {
    const listContainer = document.getElementById('medications-list');
    
    try {
        const response = await InventoryAPI.getAll();
        if (response.success) {
            const medications = response.data;
            
            if (medications.length === 0) {
                listContainer.innerHTML = '<p>No medications available.</p>';
                return;
            }
            
            const medicationsList = `
                <div class="medication-selection">
                    ${medications.map(med => `
                        <div class="medication-item">
                            <div class="med-info">
                                <h4>${med.name}</h4>
                                <p>Price: $${med.price}</p>
                            </div>
                            <div class="med-actions">
                                <button type="button" class="btn btn-sm" 
                                    onclick="addToPrescription(${med.id}, '${med.name}')">
                                    Add to Prescription
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            
            listContainer.innerHTML = medicationsList;
        } else {
            listContainer.innerHTML = `<div class="error">Failed to load medications</div>`;
        }
    } catch (error) {
        listContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

function addToPrescription(id, name) {
    // Check if medication already in prescription
    const existingItem = prescriptionItems.find(item => item.id === id);
    
    if (existingItem) {
        alert('This medication is already in the prescription');
        return;
    }
    
    prescriptionItems.push({
        id,
        name,
        dosage: '',
        instructions: ''
    });
    
    // Update the prescription display
    updatePrescriptionDisplay();
}

function updatePrescriptionDisplay() {
    const prescriptionContainer = document.getElementById('prescription-items');
    
    if (prescriptionItems.length === 0) {
        prescriptionContainer.innerHTML = '<p>No medications added to prescription</p>';
        return;
    }
    
    const prescriptionHTML = `
        <table class="table">
            <thead>
                <tr>
                    <th>Medication</th>
                    <th>Dosage</th>
                    <th>Instructions</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${prescriptionItems.map((item, index) => `
                    <tr>
                        <td>${item.name}</td>
                        <td>
                            <input type="text" name="dosage_${item.id}" 
                                placeholder="e.g., 10mg twice daily" 
                                value="${item.dosage}" 
                                onchange="updateItemDosage(${item.id}, this.value)">
                        </td>
                        <td>
                            <input type="text" name="instructions_${item.id}" 
                                placeholder="e.g., Take with food" 
                                value="${item.instructions}" 
                                onchange="updateItemInstructions(${item.id}, this.value)">
                        </td>
                        <td>
                            <button type="button" class="btn btn-sm btn-danger" 
                                onclick="removeFromPrescription(${item.id})">Remove</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
        <input type="hidden" name="prescriptionItems" value="${JSON.stringify(prescriptionItems)}">
    `;
    
    prescriptionContainer.innerHTML = prescriptionHTML;
}

function updateItemDosage(id, dosage) {
    const item = prescriptionItems.find(item => item.id === id);
    if (item) {
        item.dosage = dosage;
    }
}

function updateItemInstructions(id, instructions) {
    const item = prescriptionItems.find(item => item.id === id);
    if (item) {
        item.instructions = instructions;
    }
}

function removeFromPrescription(id) {
    const index = prescriptionItems.findIndex(item => item.id === id);
    if (index !== -1) {
        prescriptionItems.splice(index, 1);
        updatePrescriptionDisplay();
    }
}

async function handlePrescriptionSubmit(event) {
    event.preventDefault();
    
    if (prescriptionItems.length === 0) {
        alert('Please add at least one medication to the prescription');
        return;
    }
    
    // Check if all medications have dosage information
    const missingDosage = prescriptionItems.some(item => !item.dosage.trim());
    if (missingDosage) {
        alert('Please provide dosage information for all medications');
        return;
    }
    
    const formData = new FormData(event.target);
    const prescriptionData = {
        patientName: formData.get('patientName'),
        prescriptionType: formData.get('prescriptionType'),
        medications: prescriptionItems,
        notes: formData.get('notes') || '',
        validUntil: formData.get('validUntil'),
        doctor: JSON.parse(localStorage.getItem('token')).username
    };
    
    try {
        const response = await InventoryAPI.createPrescription(prescriptionData);
        if (response.success) {
            alert('Prescription created successfully!');
            // Clear prescription and redirect to prescriptions list
            prescriptionItems.length = 0;
            navigateTo('prescriptions');
        } else {
            alert(`Failed to create prescription: ${response.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}