
function populateDomainsTable(domains) {
  const tableBody = document.getElementById('domainsTable').querySelector('tbody');

  const total_domains = domains.length
  let total_verified_comains = 0

  // Loop through the data array and create a row for each item
  for (let i = 0; i < domains.length; i++) {
    const item = domains[i];

    const sslExpiration = item.ssl_expiration ? item.ssl_expiration : "N/A";

    const issuer =
      item.ssl_issuer &&
        item.ssl_issuer[1] &&
        item.ssl_issuer[1][0] &&
        item.ssl_issuer[1][0][1] ? item.ssl_issuer[1][0][1] : "N/A";

    if(issuer !== 'N/A') {
      total_verified_comains++
    }

    const row = createTableRow(item.domain, item.status, sslExpiration, issuer);

    tableBody.appendChild(row);
  }

  document.getElementById('total_domains').innerHTML = `${total_domains}`
  document.getElementById('total_verified_comains').innerHTML = `${total_verified_comains}`
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
  deleteIcon.setAttribute("data-domain", domain);
  deleteIcon.textContent = '🗑️';
  deleteIcon.onclick = async function () {
    await deleteRow(deleteIcon); // Calls the deleteRow function when clicked
  };

  async function deleteRow(deleteButton) {

    const domain = deleteIcon.getAttribute("data-domain")
    await DomainsService.getInstance().deleteDomain(domain);

    // const row = deleteButton.parentElement.parentElement;
    // row.remove();
  }

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
    event.preventDefault(); 

    const domainName = document.getElementById('domainName').value;
    const file = document.getElementById("domainsFile").files[0]; 

    const userId = LocalStorageService.getInstance().getItem('username')
    
    if(file) {
      const file = document.getElementById("domainsFile").files[0];  
      
      const formData = new FormData();  // Create a new FormData object
      formData.append("user_id", userId);  // Append the user ID to the FormData
      formData.append("file", file);  // Append the file to the FormData

      const results = await DomainsService.getInstance().uploadDomainsFile(formData);
      results.isOk && populateTable();
    }
    else {
      if (domainName) {
        const results = await DomainsService.getInstance().addDomain(domainName);
        results.isOk && populateTable();
      } else {
        alert('Please enter a domain name.');
      }
    }

    // Close modal after submission
    modal.style.display = 'none';

    // Reset the form
    addDomainForm.reset();
  })
}

handleAddDomainPopup()


function fetchForDomainsPeriodically(){
  populateTable();

  setInterval(async () => {
    console.log(`fetchForDomainsPeriodically: start populateTable()`)
    await populateTable();
  }, 5000)
}

fetchForDomainsPeriodically()
