
function populateDomainsTable(domains) {
  // Assuming there is a <table> with id="myTable"
  const table = document.getElementById("domainsTable");

  // Loop through the data array and create a row for each item
  for (let i = 0; i < domains.length; i++) {
    const item = domains[i];

    const issuer = 
      item.ssl_issuer && 
      item.ssl_issuer[1] && 
      item.ssl_issuer[1][0] &&
      item.ssl_issuer[1][0][1] ? item.ssl_issuer[1][0][1] : "N/A"

    const row = createTableRow(
      item.domain,
      item.status,
      item.ssl_expiration ? item.ssl_expiration : "N/A",
      issuer
    );
    table.appendChild(row); // Append the row to the table
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
