document.addEventListener('DOMContentLoaded', function() {
    // Check if we are on a ScraperTask change page
    const pathParts = window.location.pathname.split('/').filter(p => p !== '');
    if (pathParts.length >= 4 && pathParts[pathParts.length - 1] === 'change' && pathParts[pathParts.length - 3] === 'scrapertask') {
        const taskId = pathParts[pathParts.length - 2];
        const logsContainer = document.querySelector('.field-logs .readonly');
        
        if (logsContainer) {
            // Style it like a terminal
            logsContainer.style.backgroundColor = '#0f172a';
            logsContainer.style.color = '#4ade80';
            logsContainer.style.fontFamily = 'monospace';
            logsContainer.style.padding = '15px';
            logsContainer.style.borderRadius = '5px';
            logsContainer.style.minHeight = '300px';
            logsContainer.style.maxHeight = '600px';
            logsContainer.style.overflowY = 'auto';
            logsContainer.style.whiteSpace = 'pre-wrap';
            logsContainer.style.boxShadow = 'inset 0 0 10px rgba(0,0,0,0.5)';
            logsContainer.style.display = 'block';
            logsContainer.style.width = '100%';
            logsContainer.style.boxSizing = 'border-box';

            // Function to poll the live_logs API
            const pollLogs = function() {
                fetch(`/admin/catalog/scrapertask/${taskId}/live_logs/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.logs !== undefined) {
                            // Only update and scroll if logs actually changed
                            if (logsContainer.textContent !== data.logs) {
                                logsContainer.textContent = data.logs || 'Waiting for crawler to initialize...';
                                logsContainer.scrollTop = logsContainer.scrollHeight;
                            }
                        }
                        
                        // If status is completed or failed, we can stop polling
                        if (data.status === 'completed' || data.status === 'failed') {
                            clearInterval(pollingInterval);
                        }
                    })
                    .catch(err => console.error("Terminal Polling Error:", err));
            };

            // Poll every 1.5 seconds
            const pollingInterval = setInterval(pollLogs, 1500);
            
            // Initial poll
            pollLogs();
        }
    }
});
