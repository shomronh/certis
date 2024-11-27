
function populateDomainsTable(domains) {
  const tableBody = document.getElementById('domainsTable').querySelector('tbody');

  // Loop through the data array and create a row for each item
  for (let i = 0; i < domains.length; i++) {
    const item = domains[i];

    const sslExpiration = item.ssl_expiration ? item.ssl_expiration : "N/A";

    const issuer =
      item.ssl_issuer &&
        item.ssl_issuer[1] &&
        item.ssl_issuer[1][0] &&
        item.ssl_issuer[1][0][1] ? item.ssl_issuer[1][0][1] : "N/A";

    const row = createTableRow(item.domain, item.status, sslExpiration, issuer);

    tableBody.appendChild(row);
  }
}

// Function to create and append rows to the table
function createTableRow(domain, status, expiry, certificate) {
  // Create the <tr> element
  const tr = document.createElement("tr");

  // Create and append <td> elements to the row
  const tdDomain = document.createElement("td");
  tdDomain.textContent = domain;

  const tdStatus = document.createElement("td");
  tdStatus.textContent = status;

  const tdExpiry = document.createElement("td");
  tdExpiry.textContent = expiry;

  const tdCertificate = document.createElement("td");
  tdCertificate.textContent = certificate;

  const tdDelete = document.createElement('td');
  const deleteIcon = document.createElement('span');
  deleteIcon.classList.add('delete-icon');
  deleteIcon.textContent = '🗑️';
  deleteIcon.onclick = function () {
    deleteRow(deleteIcon); // Calls the deleteRow function when clicked
  };
  tdDelete.appendChild(deleteIcon);


  tr.appendChild(tdDomain);
  tr.appendChild(tdStatus);
  tr.appendChild(tdExpiry);
  tr.appendChild(tdCertificate);
  tr.appendChild(tdDelete);

  return tr;
}

function clearTableRows() {
  const tableBody = document.getElementById('domainsTable').querySelector('tbody');
  tableBody.innerHTML = '';
}

async function populateTable() {
  const domains = await DomainsService.getInstance().getDomains();
  clearTableRows()
  populateDomainsTable(domains);
}

populateTable();

function handleAddDomainPopup() {
  const addDomainBtn = document.getElementById('addDomainBtn');
  const modal = document.getElementById('addDomainModal');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const addDomainForm = document.getElementById('addDomainForm');
  const domainTable = document.getElementById('domainsTable').getElementsByTagName('tbody')[0];

  // Open the modal when "Add Domain" is clicked
  addDomainBtn.addEventListener('click', () => {
    modal.style.display = 'block';
  });

  // Close the modal when "Cancel" is clicked
  closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // Close the modal if the user clicks outside of it
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });

  // Handle form submission
  addDomainForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent form from refreshing the page
    const domainName = document.getElementById('domainName').value;

    if (domainName) {

      const results = await DomainsService.getInstance().addDomain(domainName);
      results.isOk && populateTable();
    } else {
      alert('Please enter a domain name.');
    }

    // Close modal after submission
    // modal.style.display = 'none';

    // Reset the form
    // addDomainForm.reset();

    // Function to delete a row
    function deleteRow(deleteButton) {
      const row = deleteButton.parentElement.parentElement; // Get the row to delete
      row.remove(); // Remove the row
      alert('Row deleted successfully!'); // Show confirmation
    }
  })
}

handleAddDomainPopup()
