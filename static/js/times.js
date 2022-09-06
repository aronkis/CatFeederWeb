 
const form = document.getElementById('feedingTimes');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const numberOfFeedTimes = document.getElementById('numberOfFeedTimes').value;
    const feedTimes = document.getElementsByClassName("feedTime");
    let times = [];
    for (let i = 0; i < numberOfFeedTimes; i++) {
        time = feedTimes[i].value;
        times.push(time);
    }
    try {
        const result = await fetch('/setFeedingHours', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "times": times })
        });
        const data = await result.json();
        consolge.log(data);
        if (result.ok) {
            location.assign('/settings');
        }
    } catch (err) {
        console.log(err);
    }
});

