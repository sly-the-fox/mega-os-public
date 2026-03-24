// Runs on LinkedIn profile pages
// Expands all sections and extracts full profile text

async function expandAllSections() {
  // Page is already loaded when button is clicked
  // Just click any visible "...see more" inline expanders
  const inlineExpandButtons = document.querySelectorAll(
    'button.inline-show-more-text__button'
  );

  for (const btn of inlineExpandButtons) {
    const btnText = btn.textContent?.toLowerCase() || '';
    const isSeeMore = btnText.includes('see more') || btnText.includes('…');
    const isInFeed = btn.closest('.feed-shared-update-v2') ||
                     btn.closest('nav') ||
                     btn.closest('header') ||
                     btn.closest('.scaffold-layout__aside');

    if (isSeeMore && !isInFeed) {
      try {
        btn.click();
        await new Promise(resolve => setTimeout(resolve, 200));
      } catch(e) {}
    }
  }

  // Brief wait for any expanded text to render
  await new Promise(resolve => setTimeout(resolve, 400));
}

function extractProfileText() {
  const main = document.querySelector('main');
  if (!main) return '';

  let text = main.innerText.trim();

  // Truncate at right-sidebar noise markers
  const noiseMarkers = [
    'More profiles for you',
    'People you may know',
    'People also viewed',
    'You might like',
    'Promoted\n',
    'Explore relevant',
    'People from',
    'People in the',
    'Invitations (',
    'Manage my network'
  ];

  for (const marker of noiseMarkers) {
    const idx = text.indexOf(marker);
    if (idx > 300) {
      text = text.substring(0, idx);
      break;
    }
  }

  // Clean up excessive blank lines
  text = text.replace(/\n{4,}/g, '\n\n').trim();

  // Limit to 8000 chars
  if (text.length > 8000) text = text.substring(0, 8000) + '\n...[truncated]';

  return text;
}

function getProfileName() {
  // Try h1 first (most reliable on actual profile pages)
  const h1 = document.querySelector('h1');
  if (h1 && h1.innerText.trim().length > 1) {
    return h1.innerText.trim();
  }

  // Fallback: extract from URL
  // e.g. linkedin.com/in/jake-costello-pt-dpt-csmt-314a8559
  const urlMatch = window.location.pathname.match(/\/in\/([^/]+)/);
  if (urlMatch) {
    const slug = urlMatch[1];
    // Remove trailing ID numbers and convert hyphens to spaces
    const cleaned = slug
      .replace(/-[a-f0-9]{6,}$/, '')  // Remove trailing hex IDs
      .replace(/-\d+$/, '')            // Remove trailing numeric IDs
      .split('-')
      .slice(0, 4)                     // Take first 4 parts (first + last name usually)
      .map(w => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ');
    return cleaned;
  }

  return 'Unknown';
}

// Listen for messages from popup
let clawbotCaptureInProgress = false;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'captureProfile') {
    if (clawbotCaptureInProgress) {
      console.log('[ClawBot] Capture already in progress, ignoring duplicate');
      return true;
    }
    clawbotCaptureInProgress = true;

    // Must return true synchronously to keep channel open for async response
    (async () => {
      const indicator = document.createElement('div');
      indicator.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 999999;
        background: #0a66c2; color: white; padding: 12px 20px;
        border-radius: 8px; font-family: sans-serif; font-size: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      `;
      indicator.textContent = '⏳ ClawBot: Expanding profile...';
      document.body.appendChild(indicator);

      try {
        await expandAllSections();

        indicator.textContent = '📤 ClawBot: Capturing profile...';

        const profileText = extractProfileText();
        const profileName = getProfileName();
        const profileUrl = window.location.href;

        console.log('[ClawBot] Name:', profileName);
        console.log('[ClawBot] Text length:', profileText.length);
        console.log('[ClawBot] Text preview:', profileText.substring(0, 200));

        const result = await new Promise((resolve, reject) => {
          chrome.runtime.sendMessage({
            action: 'sendToClawBot',
            data: { text: profileText, name: profileName, url: profileUrl }
          }, response => {
            if (chrome.runtime.lastError) {
              reject(new Error(chrome.runtime.lastError.message));
            } else {
              resolve(response);
            }
          });
        });

        if (result.success && result.result?.success) {
          indicator.style.background = '#057642';
          indicator.textContent = `✅ Saved! Generating message for ${profileName}...`;
          setTimeout(() => indicator.remove(), 4000);
          clawbotCaptureInProgress = false;
          sendResponse({ success: true });
        } else {
          throw new Error(result.error || 'Save failed');
        }

      } catch(e) {
        console.error('ClawBot capture error:', e);
        indicator.style.background = '#cc1016';
        indicator.textContent = '❌ Error: ' + e.message;
        setTimeout(() => indicator.remove(), 6000);
        clawbotCaptureInProgress = false;
        sendResponse({ success: false, error: e.message });
      }
    })();

    return true; // Keep message channel open
  }
});
