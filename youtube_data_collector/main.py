"""
Main script demonstrating the usage of YouTube Data Collector
"""

from youtube_api import YouTubeDataCollector
from data_processor import export_to_excel
import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize with API key from environment variable
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        logger.error("YouTube API key not found in environment variables")
        return
        
    collector = YouTubeDataCollector(api_key)
    
    try:
        # Read channel URLs from Excel
        logger.info("Reading channel URLs from Excel...")
        channel_urls = pd.read_excel('data/YT_channel_list.xlsx')['Channel URL'].tolist()
        
        # Clean URLs
        channel_urls = [url.split("\xa0")[0] for url in channel_urls]
        channel_urls = list(set(channel_urls))  # Remove duplicates
        logger.info(f"Found {len(channel_urls)} unique channel URLs")
        
        # Collect channel overview data
        channel_overview = []
        for url in channel_urls:
            logger.info(f"Processing channel URL: {url}")
            channel_id = collector.get_channel_id(url)
            if channel_id:
                logger.info(f"Found channel ID: {channel_id}")
                channel_details = collector.get_channel_details(channel_id)
                if channel_details:
                    channel_overview.append(channel_details)
        
        channel_overview_df = pd.DataFrame(channel_overview)
        logger.info(f"Collected overview data for {len(channel_overview)} channels")
        
        # Collect video data for each channel
        video_data = {}
        for channel_name, playlist_id in channel_overview_df[['Channel Name', 'PlaylistID']].values:
            logger.info(f"Getting videos for channel: {channel_name}")
            video_list = collector.get_video_list(playlist_id)
            if video_list:
                logger.info(f"Found {len(video_list)} videos")
                temp_df = collector.get_video_details(video_list)
                if not temp_df.empty:
                    temp_df['Channel Name'] = channel_name
                    video_data[channel_name] = temp_df
                    logger.info(f"Successfully processed {len(temp_df)} videos for {channel_name}")
                else:
                    logger.error(f"Failed to get video details for {channel_name}")
            else:
                logger.error(f"No videos found for {channel_name}")
        
        # Export data
        if video_data:
            export_to_excel(video_data, 'youtube_channel_data.xlsx')
            logger.info("Data export complete")
        else:
            logger.error("No video data collected to export")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 