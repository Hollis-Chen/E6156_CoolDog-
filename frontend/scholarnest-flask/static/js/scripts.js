document.addEventListener('DOMContentLoaded', function() {
    function handleZoteroLinkFormSubmission(e) {
        e.preventDefault();
        const userId = document.getElementById('zotero-user-id').value;
        const apiKey = document.getElementById('zotero-api-key').value;

        fetch('/link-zotero', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId, apiKey })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Data received from /link-zotero:", data);
            window.location.href = '/import-papers';
        })
        .catch(error => {
            console.error('Error linking Zotero account:', error);
            alert("Error linking Zotero account");
        });
    }

    const zoteroLinkForm = document.getElementById('zotero-link-form');
    if (zoteroLinkForm) {
        zoteroLinkForm.addEventListener('submit', handleZoteroLinkFormSubmission);
    }
});