document.addEventListener('DOMContentLoaded', () => {
    fetch('prompts.txt')
        .then(response => response.text())
        .then(data => {
            const prompts = data.split('\n').filter(prompt => prompt.trim() !== '');
            const tableBody = document.getElementById('table-body');

            prompts.forEach((prompt, index) => {
                const row = document.createElement('tr');

                const promptCell = document.createElement('td');
                promptCell.textContent = prompt;
                row.appendChild(promptCell);

                const modelACell = document.createElement('td');
                const modelAVideo = document.createElement('video');
                modelAVideo.controls = true;
                modelAVideo.src = `sora1.2/sample_${index.toString().padStart(4, '0')}.mp4`;
                modelACell.appendChild(modelAVideo);
                row.appendChild(modelACell);

                const modelBCell = document.createElement('td');
                const modelBVideo = document.createElement('video');
                modelBVideo.controls = true;
                modelBVideo.src = `sora1.2/sample_${index.toString().padStart(4, '0')}.mp4`;
                modelBCell.appendChild(modelBVideo);
                row.appendChild(modelBCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching prompts:', error));
});
