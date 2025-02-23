"""
YouTube Data Collection Module

This module provides functionality to collect data from YouTube channels using the YouTube Data API.
It allows fetching channel details and video information for specified YouTube channels.
"""

from googleapiclient.discovery import build
import pandas as pd
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeDataCollector:
    """
    A class to collect and process YouTube channel and video data.
    
    Attributes:
        api_key (str): YouTube Data API key
        youtube: YouTube API service object
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the YouTubeDataCollector with an API key.
        
        Args:
            api_key (str): YouTube Data API key
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_channel_id(self, channel_url: str) -> Optional[str]:
        """
        Extract channel ID from a YouTube channel URL.
        
        Args:
            channel_url (str): URL of the YouTube channel
            
        Returns:
            str: Channel ID if found, None otherwise
        """
        try:
            if '/channel/' in channel_url:
                return channel_url.split('/channel/')[1].split('/')[0]
            elif '/@' in channel_url:
                handle = channel_url.split('/@')[1].split('/')[0]
                request = self.youtube.search().list(
                    q=handle,
                    type='channel',
                    part='id'
                )
                response = request.execute()
                return response['items'][0]['id']['channelId']
            return None
        except Exception as e:
            logger.error(f"Error getting channel ID for {channel_url}: {str(e)}")
            return None

    def get_channel_details(self, channel_id: str) -> Dict:
        """
        Get channel details using channel ID.
        
        Args:
            channel_id (str): YouTube channel ID
            
        Returns:
            dict: Channel details including name, subscriber count, view count, etc.
        """
        try:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=channel_id
            )
            response = request.execute()

            if not response['items']:
                return {}

            channel_data = response['items'][0]
            return {
                'Channel Name': channel_data['snippet']['title'],
                'Subscriber Count': channel_data['statistics']['subscriberCount'],
                'View Count': channel_data['statistics']['viewCount'],
                'Video Count': channel_data['statistics']['videoCount'],
                'PlaylistID': channel_data['contentDetails']['relatedPlaylists']['uploads']
            }
        except Exception as e:
            logger.error(f"Error getting channel details for {channel_id}: {str(e)}")
            return {}

    def get_video_list(self, playlist_id: str) -> List[str]:
        """
        Get list of video IDs from a playlist.
        
        Args:
            playlist_id (str): YouTube playlist ID
            
        Returns:
            list: List of video IDs
        """
        video_list = []
        next_page_token = None
        
        try:
            while True:
                request = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()

                for item in response['items']:
                    video_list.append(item['contentDetails']['videoId'])

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

            return video_list
        except Exception as e:
            logger.error(f"Error getting video list for playlist {playlist_id}: {str(e)}")
            return []

    def get_video_details(self, video_list: List[str]) -> pd.DataFrame:
        """
        Get details for a list of videos.
        
        Args:
            video_list (list): List of video IDs
            
        Returns:
            pd.DataFrame: DataFrame containing video details
        """
        video_data = []
        
        try:
            for i in range(0, len(video_list), 50):
                request = self.youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(video_list[i:i+50])
                )
                response = request.execute()

                for item in response['items']:
                    video_data.append({
                        'Video ID': item['id'],
                        'Title': item['snippet']['title'],
                        'Published At': item['snippet']['publishedAt'],
                        'View Count': item['statistics'].get('viewCount', 0),
                        'Like Count': item['statistics'].get('likeCount', 0),
                        'Comment Count': item['statistics'].get('commentCount', 0),
                        'Duration': item['contentDetails']['duration']
                    })

            return pd.DataFrame(video_data)
        except Exception as e:
            logger.error(f"Error getting video details: {str(e)}")
            return pd.DataFrame() 