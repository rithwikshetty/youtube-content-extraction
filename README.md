# YouTube Content Extraction

A Python-based tool for extracting metadata from YouTube channels using the YouTube Data API. This project allows you to collect detailed information about YouTube channels and their videos in bulk, making it perfect for content analysis and research.

## Features

- Extract channel statistics (subscriber count, view count, video count)
- Collect detailed video metadata (views, likes, comments, duration)
- Support for multiple YouTube channel URLs
- Bulk data processing capabilities
- Export data to Excel with organised sheets
- Proper error handling and logging

## Prerequisites

Before you begin, ensure you have:

- Python 3.6 or higher installed
- A Google Developer account
- YouTube Data API v3 credentials
- Required Python packages (listed in requirements.txt)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-content-extraction.git
   cd youtube-content-extraction
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your YouTube API credentials:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create credentials (API key)
   - Copy your API key

4. Create a `.env` file in the root directory:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

## Project Structure

```
youtube-content-extraction/
├── youtube_data_collector/
│   ├── main.py              # Main script to run the collector
│   ├── youtube_api.py       # YouTube API interaction module
│   └── data_processor.py    # Data processing and export module
├── data/
│   └── YT_channel_list.xlsx # Input file with channel URLs
├── .env                     # Environment variables
└── README.md
```

## Usage

1. Prepare your input data:
   - Create an Excel file named `YT_channel_list.xlsx` in the `data` directory
   - Add a column named "Channel URL" containing YouTube channel URLs
   - Supported URL formats:
     - Channel URLs: `https://www.youtube.com/channel/UC...`
     - Handle URLs: `https://www.youtube.com/@channelname`

2. Run the collector:
   ```bash
   python youtube_data_collector/main.py
   ```

3. The script will:
   - Read channel URLs from your Excel file
   - Collect channel statistics
   - Gather detailed video data
   - Export everything to `youtube_channel_data.xlsx`

## Understanding the Code

### YouTubeDataCollector Class

The main functionality is implemented in the `YouTubeDataCollector` class, which provides methods to:

- Extract channel IDs from URLs
- Collect channel statistics
- Gather video metadata
- Process data in batches

Example usage:
```python
from youtube_data_collector.youtube_api import YouTubeDataCollector

# Initialize the collector
collector = YouTubeDataCollector(api_key)

# Get channel ID
channel_id = collector.get_channel_id("https://www.youtube.com/@channelname")

# Get channel details
channel_info = collector.get_channel_details(channel_id)

# Get video details
video_list = collector.get_video_list(channel_info['PlaylistID'])
video_details = collector.get_video_details(video_list)
```

### Data Processing

The `data_processor.py` module handles the export of collected data to Excel format. Each channel's data is stored in a separate worksheet for better organisation.

## Output Format

The exported Excel file contains:
- One sheet per channel
- Detailed video metrics including:
  - Video ID
  - Title
  - Publication date
  - View count
  - Like count
  - Comment count
  - Video duration

## Error Handling

The project implements comprehensive error handling and logging:
- All API interactions are wrapped in try-except blocks
- Errors are logged with detailed messages
- The script continues processing even if individual channel/video collection fails

## Rate Limits

Be mindful of YouTube API quotas:
- The API has daily quota limits
- Each API call consumes quota points
- The script processes data in batches to optimise quota usage

## Contributing

Feel free to contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting

Common issues and solutions:

1. API Key Issues:
   - Ensure your API key is correctly set in the `.env` file
   - Verify the API key has YouTube Data API v3 access

2. Rate Limiting:
   - If you hit quota limits, wait 24 hours for quota reset
   - Consider using multiple API keys for larger datasets

3. Data Collection Errors:
   - Check your input URLs are correctly formatted
   - Ensure channels are public and accessible
   - Review the logs for specific error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.
