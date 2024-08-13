document.addEventListener('DOMContentLoaded', () => {
    let currentIndex = 0;
    let prompts = [];

    const tableBody = document.getElementById('table-body');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const modelASelect = document.getElementById('modelA-select');
    const modelBSelect = document.getElementById('modelB-select');

    function createVideoElement(modelFolder, index) {
        const video = document.createElement('video');
        video.width = 620;
        video.height = 360;
        video.src = `assets/${modelFolder}/sample_${index.toString().padStart(4, '0')}.mp4`;
        video.autoplay = true;
        video.loop = true;
        video.muted = true;

        video.addEventListener('loadeddata', () => {
            video.play().catch(error => {
                console.error('Error playing video:', error);
            });
        });

        video.addEventListener('error', (e) => {
            console.error(`Error loading video ${index} for model ${modelFolder}:`, e);
        });

        return video;
    }

    function loadRow(index) {
        tableBody.innerHTML = '';

        const row = document.createElement('tr');
        const promptCell = document.createElement('td');
        promptCell.textContent = prompts[index];
        row.appendChild(promptCell);

        const modelACell = document.createElement('td');
        const modelBCell = document.createElement('td');

        const videoA = createVideoElement(modelASelect.value, index);
        const videoB = createVideoElement(modelBSelect.value, index);

        modelACell.appendChild(videoA);
        modelBCell.appendChild(videoB);

        row.appendChild(modelACell);
        row.appendChild(modelBCell);

        tableBody.appendChild(row);

        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex === prompts.length - 1;
    }

    function updateVideos() {
        console.log('Updating videos with selected models:', modelASelect.value, modelBSelect.value);
        if (tableBody.rows.length > 0) {
            const modelACell = tableBody.rows[0].cells[1];
            const modelBCell = tableBody.rows[0].cells[2];

            // Remove existing video elements
            modelACell.innerHTML = '';
            modelBCell.innerHTML = '';

            // Add new video elements based on the selected models
            const videoA = createVideoElement(modelASelect.value, currentIndex);
            const videoB = createVideoElement(modelBSelect.value, currentIndex);

            modelACell.appendChild(videoA);
            modelBCell.appendChild(videoB);
        }
    }

    fetch('assets/prompts.txt')
        .then(response => response.text())
        .then(data => {
            prompts = data.split('\n').filter(prompt => prompt.trim() !== '');
            if (prompts.length > 0) {
                loadRow(currentIndex);
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

    modelASelect.addEventListener('change', updateVideos);
    modelBSelect.addEventListener('change', updateVideos);
});
