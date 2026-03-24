// Background service worker - handles fetch requests on behalf of content scripts
// This runs outside LinkedIn's Content Security Policy restrictions

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'sendToClawBot') {
    // Make the fetch from background context (not subject to LinkedIn's CSP)
    fetch('http://127.0.0.1:7799/capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request.data)
    })
    .then(r => r.json())
    .then(result => sendResponse({ success: true, result }))
    .catch(e => sendResponse({ success: false, error: e.message }));

    return true; // Keep message channel open for async response
  }
});
