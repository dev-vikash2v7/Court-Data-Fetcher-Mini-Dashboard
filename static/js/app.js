// API utility functions
const Api = {
    post: async (url, body) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    get: async (url) => {
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};

// DOM elements
const caseSearchForm = document.getElementById('caseSearchForm');
const resultsSection = document.getElementById('resultsSection');
const caseDetails = document.getElementById('caseDetails');
const searchHistory = document.getElementById('searchHistory');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorModal = document.getElementById('errorModal');
const errorMessage = document.getElementById('errorMessage');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadSearchHistory();
    
    caseSearchForm.addEventListener('submit', handleCaseSearch);
});

// Handle case search form submission
async function handleCaseSearch(event) {
    event.preventDefault();
    
    const formData = new FormData(caseSearchForm);
    const searchData = {
        caseType: formData.get('caseType'),
        caseNumber: formData.get('caseNumber'),
        filingYear: formData.get('filingYear')
    };
    
    // Validate form data
    if (!searchData.caseType || !searchData.caseNumber || !searchData.filingYear) {
        showError('Please fill in all required fields.');
        return;
    }
    
    // Show loading overlay
    showLoading();
    
    try {
        const response = await Api.post('/api/fetch-case', searchData);
        
        if (response.success) {
            displayCaseResults(response.data);
            loadSearchHistory(); // Refresh history
        } else {
            showError(response.error || 'Failed to fetch case data.');
        }
    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Search error:', error);
    } finally {
        hideLoading();
    }
}

// Display case results
function displayCaseResults(data) {
    const caseInfoHtml = `
        <div class="case-info">
            <h4><i class="fas fa-info-circle"></i> Case Information</h4>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Case Type</div>
                    <div class="info-value">${data.case_type}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Case Number</div>
                    <div class="info-value">${data.case_number}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Status</div>
                    <div class="info-value status-${data.case_status.toLowerCase()}">${data.case_status}</div>
                </div>
            </div>
        </div>
        
        <div class="case-info">
            <h4><i class="fas fa-users"></i> Parties</h4>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Petitioner</div>
                    <div class="info-value">${data.parties.petitioner}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Respondent</div>
                    <div class="info-value">${data.parties.respondent}</div>
                </div>
            </div>
        </div>
        
        <div class="case-info">
            <h4><i class="fas fa-calendar"></i> Important Dates</h4>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Filing Date</div>
                    <div class="info-value">${formatDate(data.dates.filing_date)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Next Hearing</div>
                    <div class="info-value">${formatDate(data.dates.next_hearing)}</div>
                </div>
            </div>
        </div>
    `;
    
    const ordersHtml = `
        <div class="orders-section">
            <h4><i class="fas fa-file-pdf"></i> Orders & Judgments</h4>
            ${data.orders.map(order => `
                <div class="order-item">
                    <div class="order-info">
                        <div class="order-date">${formatDate(order.date)}</div>
                        <div class="order-title">${order.title}</div>
                    </div>
                    <button class="download-btn" onclick="downloadPdf('${order.pdf_url}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            `).join('')}
        </div>
    `;
    
    caseDetails.innerHTML = caseInfoHtml + ordersHtml;
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Download PDF function
async function downloadPdf(pdfUrl) {
    try {
        const response = await Api.post('/api/download-pdf', { pdfUrl });
        
        if (response.success) {
            // In a real implementation, this would trigger a file download
            // For now, we'll show a success message
            alert(`PDF download initiated: ${response.message}`);
        } else {
            showError(response.error || 'Failed to download PDF.');
        }
    } catch (error) {
        showError('Failed to download PDF. Please try again.');
        console.error('Download error:', error);
    }
}

// Load search history
async function loadSearchHistory() {
    try {
        const response = await Api.get('/api/query-history');
        
        if (response.success) {
            displaySearchHistory(response.history);
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// Display search history
function displaySearchHistory(history) {
    if (history.length === 0) {
        searchHistory.innerHTML = '<p style="color: #718096; font-style: italic;">No recent searches</p>';
        return;
    }
    
    const historyHtml = history.map(item => `
        <div class="history-item" onclick="loadHistoryItem('${item.caseType}', '${item.caseNumber}', '${item.filingYear}')">
            <div class="history-case">${item.caseType}/${item.caseNumber}/${item.filingYear}</div>
            <div class="history-details">Case Type: ${item.caseType}</div>
            <div class="history-timestamp">${formatTimestamp(item.timestamp)}</div>
        </div>
    `).join('');
    
    searchHistory.innerHTML = historyHtml;
}

// Load history item into form
function loadHistoryItem(caseType, caseNumber, filingYear) {
    document.getElementById('caseType').value = caseType;
    document.getElementById('caseNumber').value = caseNumber;
    document.getElementById('filingYear').value = filingYear;
    
    // Scroll to search form
    document.querySelector('.search-section').scrollIntoView({ behavior: 'smooth' });
}

// Hide results section
function hideResults() {
    resultsSection.style.display = 'none';
}

// Show loading overlay
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Show error modal
function showError(message) {
    errorMessage.textContent = message;
    errorModal.style.display = 'flex';
}

// Close error modal
function closeErrorModal() {
    errorModal.style.display = 'none';
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch (error) {
        return dateString;
    }
}

function formatTimestamp(timestamp) {
    if (!timestamp) return 'N/A';
    
    try {
        const date = new Date(timestamp);
        return date.toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        return timestamp;
    }
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    if (event.target === errorModal) {
        closeErrorModal();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeErrorModal();
        hideResults();
    }
});
