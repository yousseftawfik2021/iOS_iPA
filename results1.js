const query = new URLSearchParams(window.location.search).get('search_query')

if (query) {
    // Load the Google API client library.
    gapi.load("client", function() {
        gapi.client.setApiKey("AIzaSyBr3ogLyxkEbHeVUMI5fCzBveuKwQIW7IU");
        gapi.client.load("https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest")
            .then(() => {
                console.log("YouTube API loaded successfully.");
                getResults(query)
            }, (error) => {
                console.error("Error loading Youtube API:", error);
            });
    })

    const maxResults = 100; // Maximum number of search results to display.
    let videos = []; // Array to store fetched video data.
    
    // Asynchronously searches for videos on YouTube based on the provided query.
    async function getResults(query) {
        try {
            // Fetch search results from the YouTube API.
            const response = await gapi.client.youtube.search.list({
                "part": ["snippet"],
                "type": "video",
                "maxResults": maxResults,
                "q": query
            });
    
            // Map and store information from each search result.
            videos = response.result.items.map(item => ({
                videoId: item.id.videoId,
                channelTitle: item.snippet.channelTitle,
                publishTime: item.snippet.publishTime,
                title: item.snippet.title,
                views: 0,
                likes: 0,
                dislikes: 0
            }));
    
    
            // Render the search results on the page.
            displayResults();
        } catch (error) {
            console.error("Error during search or data fetching:", error);
        }
    }
    
    // Renders search results on the webpage.
    function displayResults() {
        const search_results = document.getElementById("searchResults");
        search_results.innerHTML = ''; // Clear previous search results if any.
    
        // Iterate over each video object to create and append search result elements.
        videos.forEach(video => {
            // Create search result element.
            const search_result = document.createElement("a");
            search_result.classList.add("search__result");
            search_result.href = `http://127.0.0.1:7775/gettubehttps://www.youtube.com/watch?v=${video.videoId}`
    
            // Create container element and append to search result.
            const container = document.createElement("div");
            container.classList.add("search__result--container");
            search_result.appendChild(container);
    
            // Create title element and append to container.
            const title = document.createElement("p");
            title.classList.add("search__result--title");
            title.innerHTML = video.title;
            container.appendChild(title);
    
            // Create info element, format text, and append to container.
            const info = document.createElement("p");
            info.classList.add("search__result--info");
            const views = video.views.toLocaleString();
    
            const date = new Intl.DateTimeFormat('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            }).format(new Date(video.publishTime));
            info.innerHTML = `• ${date}`;
            container.appendChild(info);
    
            // Create author element and append to container.
            const author = document.createElement("p");
            author.classList.add("search__result--author");
            author.innerHTML = video.channelTitle;
            container.appendChild(author);
    
            // Append search result to serach results.
            search_results.append(search_result)
        })
    }
}