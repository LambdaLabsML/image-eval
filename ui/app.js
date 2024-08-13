document.addEventListener('DOMContentLoaded', () => {
    let currentIndex = 0;
    let prompts = [];

    const tableBody = document.getElementById('table-body');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');

    const modelASelect = document.getElementById('modelA-select');
    const modelBSelect = document.getElementById('modelB-select');
    const modelAHeader = document.getElementById('modelA-header');
    const modelBHeader = document.getElementById('modelB-header');

    // Set default selections
    modelASelect.value = "sora1.1-stdit-480p";
    modelBSelect.value = "sora1.2-stdit-480p";

    function loadRow(index) {
        tableBody.innerHTML = '';  // Clear the table body

        const row = document.createElement('tr');

        const promptCell = document.createElement('td');
        promptCell.textContent = prompts[index];
        row.appendChild(promptCell);

        const modelAFolder = modelASelect.value;
        const modelBFolder = modelBSelect.value;

        const modelACell = document.createElement('td');
        const modelAVideo = document.createElement('video');
        modelAVideo.controls = true;
        modelAVideo.src = `assets/${modelAFolder}/sample_${index.toString().padStart(4, '0')}.mp4`;
        modelACell.appendChild(modelAVideo);
        row.appendChild(modelACell);

        const modelBCell = document.createElement('td');
        const modelBVideo = document.createElement('video');
        modelBVideo.controls = true;
        modelBVideo.src = `assets/${modelBFolder}/sample_${index.toString().padStart(4, '0')}.mp4`;
        modelBCell.appendChild(modelBVideo);
        row.appendChild(modelBCell);

        tableBody.appendChild(row);

        // Disable buttons if at the start or end of the prompts list
        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex === prompts.length - 1;
    }

    fetch('assets/prompts.txt')
        .then(response => response.text())
        .then(data => {
            prompts = data.split('\n').filter(prompt => prompt.trim() !== '');
            if (prompts.length > 0) {
                loadRow(currentIndex);  // Load the first row initially
            }
        })
        .catch(error => console.error('Error fetching prompts:', error));

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            loadRow(currentIndex);
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentIndex < prompts.length - 1) {
            currentIndex++;
            loadRow(currentIndex);
        }
    });

    // Update table headers and reload row when a model is changed
    function updateModelHeaders() {
        modelAHeader.textContent = `${modelASelect.value} Output`;
        modelBHeader.textContent = `${modelBSelect.value} Output`;
        loadRow(currentIndex);  // Reload the current row to apply the new model selections
    }

    modelASelect.addEventListener('change', updateModelHeaders);
    modelBSelect.addEventListener('change', updateModelHeaders);
});
