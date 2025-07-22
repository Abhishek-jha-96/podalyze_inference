import requests
import xml.etree.ElementTree as ET
import re
from typing import Optional, List, Dict

class YouTubeCaptionFetcher:
    def __init__(self, video_id: str, api_key: str):
        self.video_id = video_id
        self.api_key = api_key
    
    def fetch_transcript(self, lang: str = "en", format: str = "vtt") -> Optional[str]:
        """
        Fetch transcript using YouTube Data API v3
        
        Args:
            lang: Language code (e.g., "en", "es", "fr")
            format: Caption format ("vtt", "srt", "ttml")
        
        Returns:
            Raw transcript text or None if failed
        """
        try:
            # Step 1: Get available caption tracks
            caption_tracks = self._get_caption_tracks()
            if not caption_tracks:
                print("No caption tracks found")
                return None
            
            # Step 2: Find the desired language track
            target_track = self._find_caption_track(caption_tracks, lang)
            if not target_track:
                print(f"No caption track found for language: {lang}")
                print(f"Available languages: {[track['snippet']['language'] for track in caption_tracks]}")
                return None
            
            # Step 3: Download the actual caption content
            caption_content = self._download_captions(target_track['id'], format)
            
            # Step 4: Parse and return clean text
            if caption_content:
                return self._parse_captions(caption_content, format)
            
            return None
            
        except Exception as e:
            print(f"Error fetching transcript: {e}")
            return None
    
    def _get_caption_tracks(self) -> Optional[List[Dict]]:
        """Get list of available caption tracks"""
        url = f"https://www.googleapis.com/youtube/v3/captions"
        params = {
            'part': 'snippet',
            'videoId': self.video_id,
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        else:
            print(f"Error getting caption tracks: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def _find_caption_track(self, tracks: List[Dict], lang: str) -> Optional[Dict]:
        """Find caption track for specified language"""
        # First, look for exact language match
        for track in tracks:
            if track['snippet']['language'] == lang:
                return track
        
        # If no exact match, look for language prefix (e.g., "en" matches "en-US")
        for track in tracks:
            if track['snippet']['language'].startswith(lang):
                return track
        
        return None
    
    def _download_captions(self, caption_id: str, format: str = "vtt") -> Optional[str]:
        """Download actual caption content"""
        url = f"https://www.googleapis.com/youtube/v3/captions/{caption_id}"
        params = {
            'key': self.api_key,
            'tfmt': format  # vtt, srt, ttml
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error downloading captions: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def _parse_captions(self, caption_content: str, format: str) -> str:
        """Parse caption content and extract clean text"""
        if format.lower() == "vtt":
            return self._parse_vtt(caption_content)
        elif format.lower() == "srt":
            return self._parse_srt(caption_content)
        elif format.lower() == "ttml":
            return self._parse_ttml(caption_content)
        else:
            # Return raw content if format unknown
            return caption_content
    
    def _parse_vtt(self, vtt_content: str) -> str:
        """Parse VTT format captions"""
        lines = vtt_content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip VTT headers, timestamps, and empty lines
            if (line.startswith('WEBVTT') or 
                '-->' in line or 
                line == '' or 
                line.startswith('NOTE') or
                re.match(r'^\d+$', line)):
                continue
            
            # Remove VTT formatting tags like <c.colorE5E5E5>
            clean_line = re.sub(r'<[^>]+>', '', line)
            if clean_line:
                text_lines.append(clean_line)
        
        return ' '.join(text_lines)
    
    def _parse_srt(self, srt_content: str) -> str:
        """Parse SRT format captions"""
        lines = srt_content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip sequence numbers, timestamps, and empty lines
            if (re.match(r'^\d+$', line) or 
                '-->' in line or 
                line == ''):
                continue
            
            text_lines.append(line)
        
        return ' '.join(text_lines)
    
    def _parse_ttml(self, ttml_content: str) -> str:
        """Parse TTML/XML format captions"""
        try:
            root = ET.fromstring(ttml_content)
            text_elements = root.findall('.//{http://www.w3.org/ns/ttml}p')
            
            text_lines = []
            for elem in text_elements:
                if elem.text:
                    text_lines.append(elem.text.strip())
            
            return ' '.join(text_lines)
        except ET.ParseError:
            print("Error parsing TTML content")
            return ttml_content
    
    def get_available_languages(self) -> List[str]:
        """Get list of available caption languages"""
        tracks = self._get_caption_tracks()
        if tracks:
            return [track['snippet']['language'] for track in tracks]
        return []
    
    def get_caption_info(self) -> Optional[List[Dict]]:
        """Get detailed information about available captions"""
        tracks = self._get_caption_tracks()
        if tracks:
            info = []
            for track in tracks:
                snippet = track['snippet']
                info.append({
                    'id': track['id'],
                    'language': snippet['language'],
                    'name': snippet.get('name', ''),
                    'trackKind': snippet['trackKind'],
                    'isAutoGenerated': snippet['trackKind'] == 'asr',
                    'lastUpdated': snippet['lastUpdated']
                })
            return info
        return None
