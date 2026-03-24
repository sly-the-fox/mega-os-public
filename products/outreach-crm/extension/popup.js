document.addEventListener('DOMContentLoaded', async () => {
  const captureBtn = document.getElementById('captureBtn');
  const statusDiv = document.getElementById('status');
  const mainContent = document.getElementById('mainContent');
  const notLinkedIn = document.getElementById('notLinkedIn');

  // Check if we're on a LinkedIn profile page
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const isLinkedInProfile = tab.url && tab.url.includes('linkedin.com/in/');

  if (!isLinkedInProfile) {
    mainContent.style.display = 'none';
    notLinkedIn.style.display = 'block';
    return;
  }

  captureBtn.addEventListener('click', async () => {
    captureBtn.disabled = true;
    captureBtn.textContent = 'Capturing...';
    statusDiv.textContent = 'Connecting to page...';

    try {
      // Inject content script programmatically in case auto-inject failed
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      }).catch(() => {}); // Ignore if already injected

      // Small delay to let script initialize
      await new Promise(resolve => setTimeout(resolve, 500));

      const response = await chrome.tabs.sendMessage(tab.id, {
        action: 'captureProfile'
      });

      if (response?.success) {
        captureBtn.textContent = 'Saved!';
        statusDiv.textContent = 'Profile saved. Run /outreach in Claude Code to process.';
        statusDiv.style.color = '#4caf50';
        setTimeout(() => window.close(), 2000);
      } else {
        throw new Error(response?.error || 'Unknown error');
      }
    } catch(e) {
      captureBtn.disabled = false;
      captureBtn.textContent = 'Capture Profile';
      if (e.message.includes('Could not establish connection') ||
          e.message.includes('Receiving end does not exist')) {
        statusDiv.textContent = 'Please refresh the LinkedIn page and try again.';
      } else {
        statusDiv.textContent = 'Error: ' + e.message;
      }
      statusDiv.style.color = '#f44336';
    }
  });
});
