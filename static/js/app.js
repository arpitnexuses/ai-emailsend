// Global variables
let contacts = [];
let selectedContacts = new Set();
let campaignResults = [];

// API Base URL - works for both local and deployed environments
const API_BASE = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadContacts();
    loadCampaignStatus();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Pitch input
    const pitchInput = document.getElementById('pitch-input');
    pitchInput.addEventListener('input', validateForm);
    
    // Select all button
    document.getElementById('select-all').addEventListener('click', selectAllContacts);
    
    // Deselect all button
    document.getElementById('deselect-all').addEventListener('click', deselectAllContacts);
    
    // Send campaign button
    document.getElementById('send-campaign').addEventListener('click', sendCampaign);
    
    // Test connection button
    document.getElementById('test-connection').addEventListener('click', testConnection);
    
    // Load example button
    document.getElementById('load-example').addEventListener('click', loadExamplePitch);
}

// Load example pitch
function loadExamplePitch() {
    const examplePitch = `Hi [Name],

I came across [Company Name] and was impressed by your work in [industry/field]. I believe there could be a great opportunity for collaboration between our companies.

I'd love to schedule a quick 15-minute call to discuss how we might work together. Would you be available for a brief chat this week?

Looking forward to connecting!

Best regards,
[Your Name]`;
    
    document.getElementById('pitch-input').value = examplePitch;
    validateForm();
}

// Test connection
async function testConnection() {
    const modal = document.getElementById('connection-modal');
    const statusDiv = document.getElementById('connection-status');
    
    // Show modal
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    
    // Reset status
    statusDiv.innerHTML = `
        <div class="flex items-center justify-between">
            <span>Google Sheets:</span>
            <span class="text-gray-600">Testing...</span>
        </div>
        <div class="flex items-center justify-between">
            <span>OpenAI API:</span>
            <span class="text-gray-600">Testing...</span>
        </div>
        <div class="flex items-center justify-between">
            <span>Email Config:</span>
            <span class="text-gray-600">Testing...</span>
        </div>
        <div class="flex items-center justify-between">
            <span>Contacts Found:</span>
            <span class="text-gray-600">Testing...</span>
        </div>
    `;
    
    try {
        const response = await fetch(`${API_BASE}/test-connection`);
        const data = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = `
                <div class="flex items-center justify-between">
                    <span>Google Sheets:</span>
                    <span class="text-green-600 font-medium">✓ Connected</span>
                </div>
                <div class="flex items-center justify-between">
                    <span>OpenAI API:</span>
                    <span class="text-green-600 font-medium">✓ Connected</span>
                </div>
                <div class="flex items-center justify-between">
                    <span>Email Config:</span>
                    <span class="${data.email_config === 'Configured' ? 'text-green-600' : 'text-yellow-600'} font-medium">${data.email_config === 'Configured' ? '✓ Configured' : '⚠ Not configured'}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span>Contacts Found:</span>
                    <span class="text-blue-600 font-medium">${data.contact_count}</span>
                </div>
            `;
        } else {
            statusDiv.innerHTML = `
                <div class="flex items-center justify-between">
                    <span>Google Sheets:</span>
                    <span class="text-red-600 font-medium">✗ Error</span>
                </div>
                <div class="flex items-center justify-between">
                    <span>OpenAI API:</span>
                    <span class="text-red-600 font-medium">✗ Error</span>
                </div>
                <div class="flex items-center justify-between">
                    <span>Email Config:</span>
                    <span class="text-red-600 font-medium">✗ Error</span>
                </div>
                <div class="flex items-center justify-between">
                    <span>Contacts Found:</span>
                    <span class="text-red-600 font-medium">0</span>
                </div>
            `;
        }
    } catch (error) {
        statusDiv.innerHTML = `
            <div class="flex items-center justify-between">
                <span>Connection:</span>
                <span class="text-red-600 font-medium">✗ Failed</span>
            </div>
            <div class="text-sm text-gray-600 mt-2">
                ${error.message}
            </div>
        `;
    }
}

// Close connection modal
function closeConnectionModal() {
    document.getElementById('connection-modal').classList.add('hidden');
    document.getElementById('connection-modal').classList.remove('flex');
}

// Load contacts from API
async function loadContacts() {
    try {
        const response = await fetch(`${API_BASE}/contacts`);
        const data = await response.json();
        
        if (response.ok) {
            contacts = data.contacts;
            renderContactsList();
            validateForm();
        } else {
            showError('Failed to load contacts: ' + data.error);
        }
    } catch (error) {
        showError('Failed to load contacts: ' + error.message);
    }
}

// Load campaign status
async function loadCampaignStatus() {
    try {
        const response = await fetch(`${API_BASE}/campaign-status`);
        const data = await response.json();
        
        if (response.ok) {
            updateStatusCards(data);
        } else {
            console.error('Failed to load campaign status:', data.error);
        }
    } catch (error) {
        console.error('Failed to load campaign status:', error);
    }
}

// Render contacts list
function renderContactsList() {
    const contactsList = document.getElementById('contacts-list');
    
    if (contacts.length === 0) {
        contactsList.innerHTML = `
            <div class="text-center text-gray-500 py-4">
                <i class="fas fa-users text-xl mb-2"></i>
                <p>No contacts found</p>
            </div>
        `;
        return;
    }
    
    contactsList.innerHTML = contacts.map(contact => `
        <div class="flex items-center space-x-3 py-2 border-b border-gray-200 last:border-b-0">
            <input 
                type="checkbox" 
                id="contact-${contact.id}" 
                value="${contact.id}"
                class="contact-checkbox rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                ${contact.status.includes('Sent') ? 'disabled' : ''}
            >
            <div class="flex-1">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="font-medium text-gray-900">${contact.firstname} ${contact.lastname}</p>
                        <p class="text-sm text-gray-600">${contact.email}</p>
                        <p class="text-xs text-gray-500">${contact.company_name}</p>
                    </div>
                    <div class="text-right">
                        ${getStatusBadge(contact.status)}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    // Add event listeners to checkboxes
    document.querySelectorAll('.contact-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                selectedContacts.add(parseInt(this.value));
            } else {
                selectedContacts.delete(parseInt(this.value));
            }
            updateSelectedCount();
            validateForm();
        });
    });
    
    updateSelectedCount();
}

// Update selected count
function updateSelectedCount() {
    const countElement = document.getElementById('selected-count');
    countElement.textContent = `${selectedContacts.size} selected`;
}

// Get status badge HTML
function getStatusBadge(status) {
    if (status.includes('Sent')) {
        return '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Sent</span>';
    } else if (status.includes('Failed')) {
        return '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">Failed</span>';
    } else {
        return '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">Pending</span>';
    }
}

// Select all contacts
function selectAllContacts() {
    document.querySelectorAll('.contact-checkbox:not(:disabled)').forEach(checkbox => {
        checkbox.checked = true;
        selectedContacts.add(parseInt(checkbox.value));
    });
    updateSelectedCount();
    validateForm();
}

// Deselect all contacts
function deselectAllContacts() {
    document.querySelectorAll('.contact-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
    selectedContacts.clear();
    updateSelectedCount();
    validateForm();
}

// Validate form and enable/disable send button
function validateForm() {
    const pitchInput = document.getElementById('pitch-input');
    const sendButton = document.getElementById('send-campaign');
    
    const hasPitch = pitchInput.value.trim().length > 0;
    const hasSelectedContacts = selectedContacts.size > 0;
    
    sendButton.disabled = !(hasPitch && hasSelectedContacts);
    
    if (sendButton.disabled) {
        sendButton.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        sendButton.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// Send campaign
async function sendCampaign() {
    const pitchInput = document.getElementById('pitch-input');
    const pitch = pitchInput.value.trim();
    
    if (!pitch || selectedContacts.size === 0) {
        showError('Please enter a pitch and select at least one contact.');
        return;
    }
    
    // Show loading modal
    showLoadingModal('Sending campaign...');
    
    try {
        const response = await fetch(`${API_BASE}/send-campaign`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pitch: pitch,
                contact_ids: Array.from(selectedContacts)
            })
        });
        
        const data = await response.json();
        
        hideLoadingModal();
        
        if (response.ok) {
            campaignResults = data.results;
            showSuccessModal(data.message);
            renderCampaignResults();
            loadCampaignStatus();
            
            // Clear form
            pitchInput.value = '';
            deselectAllContacts();
        } else {
            showError(data.error || 'Failed to send campaign');
        }
    } catch (error) {
        hideLoadingModal();
        showError('Failed to send campaign: ' + error.message);
    }
}

// Render campaign results
function renderCampaignResults() {
    const resultsContainer = document.getElementById('campaign-results');
    
    if (campaignResults.length === 0) {
        resultsContainer.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-chart-bar text-4xl mb-4"></i>
                <p>No campaign results yet</p>
                <p class="text-sm">Send a campaign to see results here</p>
            </div>
        `;
        return;
    }
    
    const successCount = campaignResults.filter(r => r.status === 'Sent').length;
    const failedCount = campaignResults.filter(r => r.status === 'Failed').length;
    
    resultsContainer.innerHTML = `
        <div class="mb-4 p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="font-bold text-gray-900">Campaign Summary</h3>
                    <p class="text-sm text-gray-600">${campaignResults.length} contacts processed</p>
                </div>
                <div class="flex space-x-2">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        ${successCount} Sent
                    </span>
                    ${failedCount > 0 ? `
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            ${failedCount} Failed
                        </span>
                    ` : ''}
                </div>
            </div>
        </div>
        <div class="space-y-3 max-h-96 overflow-y-auto">
            ${campaignResults.map(result => `
                <div class="border border-gray-200 rounded-lg p-4">
                    <div class="flex items-start justify-between">
                        <div class="flex-1">
                            <h4 class="font-medium text-gray-900">${result.name}</h4>
                            <p class="text-sm text-gray-600">${result.email}</p>
                            <p class="text-xs text-gray-500 mt-1">Subject: ${result.subject}</p>
                        </div>
                        <div class="ml-4">
                            ${getStatusBadge(result.status)}
                        </div>
                    </div>
                    <div class="mt-3 text-sm text-gray-700 bg-gray-50 p-3 rounded">
                        <p class="font-medium mb-1">Email Preview:</p>
                        <p class="text-gray-600">${result.body.substring(0, 150)}${result.body.length > 150 ? '...' : ''}</p>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

// Update status cards
function updateStatusCards(data) {
    document.getElementById('total-contacts').textContent = data.total_contacts;
    document.getElementById('sent-count').textContent = data.sent;
    document.getElementById('pending-count').textContent = data.pending;
    document.getElementById('failed-count').textContent = data.failed;
}

// Show loading modal
function showLoadingModal(message) {
    document.getElementById('loading-message').textContent = message;
    document.getElementById('loading-modal').classList.remove('hidden');
    document.getElementById('loading-modal').classList.add('flex');
}

// Hide loading modal
function hideLoadingModal() {
    document.getElementById('loading-modal').classList.add('hidden');
    document.getElementById('loading-modal').classList.remove('flex');
}

// Show success modal
function showSuccessModal(message) {
    document.getElementById('success-message').textContent = message;
    document.getElementById('success-modal').classList.remove('hidden');
    document.getElementById('success-modal').classList.add('flex');
}

// Close success modal
function closeSuccessModal() {
    document.getElementById('success-modal').classList.add('hidden');
    document.getElementById('success-modal').classList.remove('flex');
}

// Show error modal
function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-modal').classList.remove('hidden');
    document.getElementById('error-modal').classList.add('flex');
}

// Close error modal
function closeErrorModal() {
    document.getElementById('error-modal').classList.add('hidden');
    document.getElementById('error-modal').classList.remove('flex');
}

// Auto-refresh status every 30 seconds
setInterval(loadCampaignStatus, 30000); 