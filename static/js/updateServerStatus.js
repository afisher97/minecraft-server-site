
    /**
     * Fetch server status from the Flask API and update the HTML elements.
     * @param {string} serverName - e.g. "buildcraft" or "savagelands"
     */
    function updateServerStatus(serverName) {
      fetch(`/api/server_status/${serverName}`)
        .then(response => response.json())
        .then(data => {
          const playersEl = document.getElementById(`${serverName}-players`);
          const statusEl = document.getElementById(`${serverName}-status`);
          const playersSampleEl = document.getElementById(`${serverName}-players-sample`);

          // If the server is offline or unreachable
          if (data.error) {
            playersEl.textContent = '';
            statusEl.textContent = 'Offline';
            statusEl.classList.remove('online');
            statusEl.classList.add('offline');
            // Clear any previous player list
            playersSampleEl.innerHTML = '';

          } else {
            // Handle the player count
            const count = data.players_online;
            if (count > 0) {
              playersEl.textContent = count + (count === 1 ? ' player' : ' players');
            } else {
              playersEl.textContent = '';
            }

            // Mark the server as online
            statusEl.textContent = 'Online';
            statusEl.classList.remove('offline');
            statusEl.classList.add('online');

            // Populate the player list
            playersSampleEl.innerHTML = '';
            data.players_sample.forEach(player => {
              const li = document.createElement('li');
              li.textContent = player;
              playersSampleEl.appendChild(li);
            });
          }
        })
        .catch(err => {
          console.error(`Error fetching status for ${serverName}:`, err);
        });
    }

    // On page load, fetch statuses for each server
    document.addEventListener('DOMContentLoaded', () => {
      updateServerStatus('buildcraft');
      updateServerStatus('savagelands');
    });
