// Fetch data from the API endpoint
fetch("/api/patient_management")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("clientsTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create a delete button cell
      const deleteButtonCell = document.createElement("td");
      const deleteButton = document.createElement("button");
      deleteButton.className = "btn btn-danger";
      deleteButton.textContent = "Delete";
      // Add a click event listener to the button
      deleteButton.addEventListener("click", function () {
        // Get the clientId from the same row as the clicked button
        const clientId = this.closest("tr").cells[1].textContent;

        // Call the function to handle confirmation and deletion
        confirmAndDelete(clientId);
      });
      deleteButtonCell.appendChild(deleteButton);
      row.appendChild(deleteButtonCell);

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/provider_management")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("providersTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create a delete button cell
      const deleteButtonCell = document.createElement("td");
      const deleteButton = document.createElement("button");
      deleteButton.className = "btn btn-danger";
      deleteButton.textContent = "Delete";
      deleteButton.addEventListener("click", () => handleDelete(client.id)); // Assuming client ID is available in the data
      deleteButtonCell.appendChild(deleteButton);
      row.appendChild(deleteButtonCell);

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/employee_management")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("employeeTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create a delete button cell
      const deleteButtonCell = document.createElement("td");
      const deleteButton = document.createElement("button");
      deleteButton.className = "btn btn-danger";
      deleteButton.textContent = "Delete";
      deleteButton.addEventListener("click", () => handleDelete(client.id)); // Assuming client ID is available in the data
      deleteButtonCell.appendChild(deleteButton);
      row.appendChild(deleteButtonCell);

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Function to update the navbar based on user authentication status
function updateNavbar(authenticated, username) {
  const loginLink = document.getElementById("loginLink");
  const signOutLink = document.getElementById("signOutLink");
  const usernameElement = document.getElementById("username");

  if (authenticated) {
    // User is authenticated
    loginLink.style.display = "none";
    signOutLink.style.display = "block";
    usernameElement.textContent = username;
  } else {
    // User is not authenticated
    loginLink.style.display = "block";
    signOutLink.style.display = "none";
  }
}

// Function to check authentication status when the page loads
function checkAuthentication() {
  
  const response = {
    authenticated: true, // Change to false to simulate an unauthenticated user
    username: "Luffy", // Replace with the actual username
  };

  // Update the navbar based on the authentication status
  updateNavbar(response.authenticated, response.username);
}

// Check authentication when the page loads
document.addEventListener("DOMContentLoaded", checkAuthentication);

function confirmAndDelete(clientId) {
  const confirmed = window.confirm(
    "Are you sure you want to delete this record?"
  );

  if (confirmed) {
    // Send a request to the server to delete the record with the specified client ID
    fetch(`/api/delete_patient/${clientId}`, { method: "DELETE" })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        } else {
          console.error("Error deleting record:", response.status);
        }
      })
      .catch((error) => console.error("Error deleting record:", error));
  }
}


// Fetch data from the API endpoint
fetch("/api/query_one")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryOneTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_two")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryTwoTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_three")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryThreeTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_four")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryFourTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_five")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryFiveTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_six")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("querySixTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_seven")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("querySevenTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_eight")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryEightTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_nine")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryNineTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Fetch data from the API endpoint
fetch("/api/query_ten")
  .then((response) => response.json())
  .then((clients) => {
    // Get the table body element
    const tableBody = document.getElementById("queryTenTableBody");

    // Iterate through the clients and create table rows
    clients.forEach((client) => {
      const row = document.createElement("tr");

      // Create cells for each attribute
      for (let i = 0; i < client.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = client[i];
        row.appendChild(cell);
      }

      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch((error) => console.error("Error fetching clients:", error));

// Event listener for the button click
document.getElementById("queryOneModal").addEventListener("click", openModal);
