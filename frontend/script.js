document.addEventListener('DOMContentLoaded', () => {
    const arenaTab = document.getElementById('arena-tab');
    const leaderboardTab = document.getElementById('leaderboard-tab');
    const arenaSection = document.getElementById('arena-section');
    const leaderboardSection = document.getElementById('leaderboard-section');

    arenaTab.addEventListener('click', () => {
        arenaTab.classList.add('active');
        leaderboardTab.classList.remove('active');
        arenaSection.classList.add('active');
        leaderboardSection.classList.remove('active');
    });

    leaderboardTab.addEventListener('click', () => {
        leaderboardTab.classList.add('active');
        arenaTab.classList.remove('active');
        leaderboardSection.classList.add('active');
        arenaSection.classList.remove('active');
    });

    let currentIndex = 0;
    let prompts = [];
    let clickedVideos = [];

    const savedClickedVideos = localStorage.getItem('clickedVideos');
    if (savedClickedVideos) {
        clickedVideos = JSON.parse(savedClickedVideos);
    }

    const tableBody = document.getElementById('table-body');
    const promptDisplay = document.getElementById('prompt-display');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const modelASelect = document.getElementById('modelA-select');
    const modelBSelect = document.getElementById('modelB-select');
    const progressBar = document.getElementById('progress-bar');

    function updateProgressBar() {
        const progress = ((currentIndex + 1) / prompts.length) * 100;
        progressBar.value = progress;
    }

    function createVideoElement(modelFolder, index, model, prompt) {
        const container = document.createElement('div');
        container.className = 'video-container';

        const video = document.createElement('video');
        video.width = 620;
        video.height = 360;
        video.src = `assets/${modelFolder}/sample_${index.toString().padStart(4, '0')}.mp4`;
        video.autoplay = true;
        video.loop = true;
        video.muted = true;

        const overlay = document.createElement('div');
        overlay.className = 'overlay';
        overlay.innerHTML = '✔';

        const savedVideo = clickedVideos.find(
            v => v.prompt === prompt && v.model === model
        );
        if (savedVideo && savedVideo.isChecked) {
            container.classList.add('checked');
        }

        container.appendChild(video);
        container.appendChild(overlay);

        video.addEventListener('loadeddata', () => {
            video.play().catch(error => {
                console.error('Error playing video:', error);
            });
        });

        video.addEventListener('error', (e) => {
            console.error(`Error loading video ${index} for model ${modelFolder}:`, e);
        });

        container.addEventListener('click', () => {
            container.classList.toggle('checked');
            const isChecked = container.classList.contains('checked');

            const videoObject = clickedVideos.find(
                v => v.prompt === prompt && v.model === model
            );

            if (videoObject) {
                videoObject.isChecked = isChecked;
            } else {
                clickedVideos.push({ prompt: prompt, model: model, isChecked: isChecked });
            }

            localStorage.setItem('clickedVideos', JSON.stringify(clickedVideos));

            console.log(clickedVideos);  // This is for debugging purposes
        });

        return container;
    }

    function loadRow(index) {
        tableBody.innerHTML = '';

        const promptText = prompts[index];
        promptDisplay.textContent = `"${promptText}"`;

        const row = document.createElement('tr');

        const modelACell = document.createElement('td');
        const modelBCell = document.createElement('td');

        const videoAContainer = createVideoElement(modelASelect.value, index, modelASelect.value, promptText);
        const videoBContainer = createVideoElement(modelBSelect.value, index, modelBSelect.value, promptText);

        modelACell.appendChild(videoAContainer);
        modelBCell.appendChild(videoBContainer);

        row.appendChild(modelACell);
        row.appendChild(modelBCell);

        tableBody.appendChild(row);

        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex === prompts.length - 1;

        updateProgressBar();
    }

    function updateVideos() {
        if (tableBody.rows.length > 0) {
            const modelACell = tableBody.rows[0].cells[0];
            const modelBCell = tableBody.rows[0].cells[1];

            modelACell.innerHTML = '';
            modelBCell.innerHTML = '';

            const promptText = prompts[currentIndex];
            const videoAContainer = createVideoElement(modelASelect.value, currentIndex, modelASelect.value, promptText);
            const videoBContainer = createVideoElement(modelBSelect.value, currentIndex, modelBSelect.value, promptText);

            modelACell.appendChild(videoAContainer);
            modelBCell.appendChild(videoBContainer);
        }
    }

    function updateModelSelectOptions() {
        const modelAValue = modelASelect.value;
        const modelBValue = modelBSelect.value;

        Array.from(modelASelect.options).forEach(option => {
            option.disabled = option.value === modelBValue;
        });

        Array.from(modelBSelect.options).forEach(option => {
            option.disabled = option.value === modelAValue;
        });
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

    modelASelect.addEventListener('change', () => {
        updateModelSelectOptions();
        updateVideos();
    });

    modelBSelect.addEventListener('change', () => {
        updateModelSelectOptions();
        updateVideos();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowLeft' && !prevButton.disabled) {
            prevButton.click();
        } else if (event.key === 'ArrowRight' && !nextButton.disabled) {
            nextButton.click();
        }
    });

    updateModelSelectOptions();  // Initial call to set the correct state
});
