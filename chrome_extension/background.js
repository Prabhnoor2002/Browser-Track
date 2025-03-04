let meetingActive = false;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message === 'start_meeting') {
        meetingActive = true;
        trackTabs();
    } else if (message === 'stop_meeting') {
        meetingActive = false;
    }
});

function sendTabInfo(tab) {
    fetch('http://127.0.0.1:5000/update_tabs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tabs: [{
                title: tab.title || 'No title',
                url: tab.url || 'No URL'
            }]
        })
    }).then(response => response.json())
      .then(data => console.log('Sent tab:', data))
      .catch(error => console.error('Error sending tab info:', error));
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        sendTabInfo(tab);
    }
});

chrome.tabs.onCreated.addListener((tab) => {
    sendTabInfo(tab);
});

async function sendTabsToServer() {
    chrome.tabs.query({}, function(tabs) {
        const tabsInfo = tabs.map(tab => ({
            title: tab.title,
            url: tab.url
        }));

        fetch('http://127.0.0.1:5000/is_meeting_active')
            .then(res => res.json())
            .then(status => {
                if (status.active) {
                    fetch('http://127.0.0.1:5000/update_tabs', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ tabs: tabsInfo })
                    });
                }
            })
            .catch(err => console.error("Error checking meeting status:", err));
    });
}

chrome.tabs.onActivated.addListener(activeInfo => {
    sendTabsToServer();
});

chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
    sendTabsToServer();
});
