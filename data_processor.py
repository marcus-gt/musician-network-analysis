"""
Data processing module for musician network analysis.
Handles CSV loading, musician parsing, and network data generation.
"""

import pandas as pd
import re
from collections import defaultdict


def load_collection_data(csv_path):
    """Load vinyl collection data from CSV file."""
    return pd.read_csv(csv_path)


def parse_musicians(musicians_str, main_artist):
    """
    Parse musician string into individual musician entries with roles.
    
    Args:
        musicians_str: String containing musician data in format:
                      "Name (optional number) (roles); Name2 (roles)"
        main_artist: Main artist for this record
        
    Returns:
        List of dictionaries with musician, role, and main_artist
    """
    if pd.isna(musicians_str):
        return []
    
    musician_entries = musicians_str.split(';')
    parsed_data = []
    
    for entry in musician_entries:
        entry = entry.strip()
        if not entry:
            continue
            
        # Pattern: Name (optional number) (roles)
        pattern = r'^([^(]+?)(?:\s*\((\d+)\))?\s*\(([^)]+)\)$'
        match = re.match(pattern, entry)
        
        if match:
            name = match.group(1).strip()
            number = match.group(2)
            roles_str = match.group(3)
            
            full_name = f"{name} ({number})" if number else name
            roles = [role.strip() for role in roles_str.split(',')]
            
            for role in roles:
                if role:
                    parsed_data.append({
                        'musician': full_name,
                        'role': role,
                        'main_artist': main_artist
                    })
    
    return parsed_data


def create_network_data(collection_df):
    """
    Create network dataset from collection dataframe.
    
    Returns:
        pandas.DataFrame with columns: musician, role, main_artist, album
    """
    all_connections = []
    
    for idx, row in collection_df.iterrows():
        main_artist = row['Artist']
        musicians_str = row['Musicians']
        album = row['Album']
        
        connections = parse_musicians(musicians_str, main_artist)
        
        for connection in connections:
            connection['album'] = album
            all_connections.append(connection)
    
    return pd.DataFrame(all_connections)


def clean_role_name(role):
    """Remove bracket information from role names to group similar roles."""
    if pd.isna(role):
        return role
    # Remove everything in brackets and parentheses
    cleaned = re.sub(r'\s*\[.*?\]', '', str(role))
    cleaned = re.sub(r'\s*\(.*?\)', '', cleaned)
    return cleaned.strip()


def create_echarts_network_data(network_df, collection_df):
    """
    Create complete data structure for ECharts with proper node categorization.
    
    Returns:
        Dictionary with nodes, links, categories, genres, styles, and clean_roles
    """
    # Add cleaned role names
    filtered_df = network_df.copy()
    filtered_df['clean_role'] = filtered_df['role'].apply(clean_role_name)
    
    # Get all main artists
    main_artists = set(filtered_df['main_artist'].unique())
    
    # Create artist-to-genre/style mapping
    artist_info = {}
    for _, row in collection_df.iterrows():
        artist = row['Artist']
        genres = str(row['Genres']) if pd.notna(row['Genres']) else ''
        styles = str(row['Styles']) if pd.notna(row['Styles']) else ''
        
        if artist not in artist_info:
            artist_info[artist] = {
                'genres': set(),
                'styles': set(),
                'albums': []
            }
        
        # Parse genres and styles
        if genres:
            genre_list = [g.strip() for g in genres.split(',')]
            artist_info[artist]['genres'].update(genre_list)
        
        if styles:
            style_list = [s.strip() for s in styles.split(',')]
            artist_info[artist]['styles'].update(style_list)
            
        artist_info[artist]['albums'].append(row['Album'])
    
    # Convert sets to lists for JSON serialization
    for artist in artist_info:
        artist_info[artist]['genres'] = list(artist_info[artist]['genres'])
        artist_info[artist]['styles'] = list(artist_info[artist]['styles'])
    
    # Create nodes
    nodes = []
    node_ids = set()
    
    # Add all main artists as artist nodes (blue)
    for artist in filtered_df['main_artist'].unique():
        if artist not in node_ids:
            musician_count = filtered_df[filtered_df['main_artist'] == artist]['musician'].nunique()
            
            artist_genres = artist_info.get(artist, {}).get('genres', [])
            artist_styles = artist_info.get(artist, {}).get('styles', [])
            artist_albums = artist_info.get(artist, {}).get('albums', [])
            
            # Get roles for this artist
            artist_roles = filtered_df[filtered_df['main_artist'] == artist]['clean_role'].unique().tolist()
            
            nodes.append({
                'id': artist,
                'name': artist,
                'category': 'artist',
                'symbolSize': min(12 + musician_count * 1.5, 35),
                'value': musician_count,
                'genres': artist_genres,
                'styles': artist_styles,
                'albums': artist_albums,
                'roles': artist_roles
            })
            node_ids.add(artist)
    
    # Add musicians who are NOT main artists as musician nodes (orange)
    for musician in filtered_df['musician'].unique():
        if musician not in node_ids:
            artist_count = filtered_df[filtered_df['musician'] == musician]['main_artist'].nunique()
            
            # Get genres/styles from artists this musician works with
            musician_artists = filtered_df[filtered_df['musician'] == musician]['main_artist'].unique()
            musician_genres = set()
            musician_styles = set()
            
            for artist in musician_artists:
                if artist in artist_info:
                    musician_genres.update(artist_info[artist]['genres'])
                    musician_styles.update(artist_info[artist]['styles'])
            
            # Get roles for this musician
            musician_roles = filtered_df[filtered_df['musician'] == musician]['clean_role'].unique().tolist()
            
            nodes.append({
                'id': musician,
                'name': musician,
                'category': 'musician',
                'symbolSize': min(8 + artist_count * 2, 25),
                'value': artist_count,
                'genres': list(musician_genres),
                'styles': list(musician_styles),
                'collaborations': list(musician_artists),
                'roles': musician_roles
            })
            node_ids.add(musician)
    
    # Create links
    links = []
    link_counts = defaultdict(int)
    
    for _, row in filtered_df.iterrows():
        musician = row['musician']
        artist = row['main_artist']
        role = row['role']
        clean_role = row['clean_role']
        album = row['album']
        
        # Only create links if both nodes exist
        if musician in node_ids and artist in node_ids:
            link_key = f"{musician}_{artist}"
            link_counts[link_key] += 1
            
            if link_counts[link_key] == 1:
                # Get genres/styles for this connection
                connection_genres = artist_info.get(artist, {}).get('genres', [])
                connection_styles = artist_info.get(artist, {}).get('styles', [])
                
                links.append({
                    'source': musician,
                    'target': artist,
                    'value': 1,
                    'roles': [role],
                    'clean_roles': [clean_role],
                    'albums': [album],
                    'genres': connection_genres,
                    'styles': connection_styles
                })
            else:
                # Find existing link and add role/album
                for link in links:
                    if link['source'] == musician and link['target'] == artist:
                        link['roles'].append(role)
                        link['clean_roles'].append(clean_role)
                        link['albums'].append(album)
                        link['value'] += 1
                        break
    
    # Get all unique genres, styles, and clean roles for filters
    all_genres = set()
    all_styles = set()
    all_clean_roles = set()
    
    for node in nodes:
        all_genres.update(node.get('genres', []))
        all_styles.update(node.get('styles', []))
        all_clean_roles.update(node.get('roles', []))
    
    categories = [
        {'name': 'musician', 'itemStyle': {'color': '#ff7f0e'}},
        {'name': 'artist', 'itemStyle': {'color': '#1f77b4'}}
    ]
    
    return {
        'nodes': nodes,
        'links': links,
        'categories': categories,
        'genres': sorted(list(all_genres)),
        'styles': sorted(list(all_styles)),
        'clean_roles': sorted(list(all_clean_roles))
    } 
