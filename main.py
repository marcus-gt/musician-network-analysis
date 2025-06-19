#!/usr/bin/env python3
"""
Main script for musician network analysis.
Orchestrates data processing, analysis, and HTML generation.
"""

import sys
import argparse
from pathlib import Path

from data_processor import (
    load_collection_data, 
    create_network_data, 
    create_echarts_network_data
)
from analysis import (
    analyze_top_musicians,
    get_session_musicians,
    get_collaboration_stats
)
from html_generator import generate_html_file
import config


def main():
    """Main function to run the complete analysis pipeline."""
    parser = argparse.ArgumentParser(
        description='Generate interactive musician network visualization'
    )
    parser.add_argument(
        '--input', '-i', 
        type=str, 
        default=config.DEFAULT_CSV_PATH,
        help=f'Input CSV file path (default: {config.DEFAULT_CSV_PATH})'
    )
    parser.add_argument(
        '--output', '-o', 
        type=str, 
        default=config.DEFAULT_OUTPUT_PATH,
        help=f'Output HTML file path (default: {config.DEFAULT_OUTPUT_PATH})'
    )
    parser.add_argument(
        '--save-csvs', 
        action='store_true',
        help='Save intermediate CSV files (network data and triples)'
    )
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input).exists():
        print(f"❌ Error: Input file '{args.input}' not found!")
        sys.exit(1)
    
    if args.verbose:
        print("🎵 Musician Network Analysis")
        print("=" * 50)
        print(f"📂 Input file: {args.input}")
        print(f"📄 Output file: {args.output}")
        print()
    
    try:
        # Step 1: Load data
        if args.verbose:
            print("⚙️  Step 1: Loading collection data...")
        collection_df = load_collection_data(args.input)
        if args.verbose:
            print(f"✅ Loaded {len(collection_df)} records")
        
        # Step 2: Create network data
        if args.verbose:
            print("⚙️  Step 2: Processing musician network...")
        network_df = create_network_data(collection_df)
        if args.verbose:
            print(f"✅ Created network with {len(network_df)} connections")
            print(f"   • {network_df['musician'].nunique()} unique musicians")
            print(f"   • {network_df['main_artist'].nunique()} main artists")
        
        # Step 3: Create ECharts network data
        if args.verbose:
            print("⚙️  Step 3: Generating network visualization data...")
        echarts_data = create_echarts_network_data(network_df, collection_df)
        if args.verbose:
            print(f"✅ Network data prepared:")
            print(f"   • {len(echarts_data['nodes'])} nodes")
            print(f"   • {len(echarts_data['links'])} links")
            print(f"   • {len(echarts_data['genres'])} genres")
            print(f"   • {len(echarts_data['styles'])} styles")
        
        # Step 4: Analyze musicians
        if args.verbose:
            print("⚙️  Step 4: Analyzing musician statistics...")
        musician_stats_df = analyze_top_musicians(network_df, collection_df)
        session_musicians_df = get_session_musicians(
            musician_stats_df,
            min_records=config.SESSION_MUSICIAN_MIN_RECORDS,
            min_session_ratio=config.SESSION_MUSICIAN_MIN_RATIO
        )
        
        if args.verbose:
            print(f"✅ Analysis complete:")
            print(f"   • {len(musician_stats_df)} musicians analyzed")
            print(f"   • {len(session_musicians_df)} session musicians found")
        
        # Step 5: Generate HTML
        if args.verbose:
            print("⚙️  Step 5: Generating interactive HTML...")
        
        # Convert DataFrames to dictionaries for JSON serialization
        musician_stats_data = musician_stats_df.to_dict('records')
        session_musicians_data = session_musicians_df.to_dict('records')
        
        output_file = generate_html_file(
            network_data=echarts_data,
            musician_stats_data=musician_stats_data,
            session_musicians_data=session_musicians_data,
            output_path=args.output
        )
        
        if args.verbose:
            print(f"✅ HTML file generated: {output_file}")
        
        # Step 6: Save CSV files if requested
        if args.save_csvs:
            if args.verbose:
                print("⚙️  Step 6: Saving CSV files...")
            
            # Save network data
            network_df.to_csv(config.NETWORK_CSV_PATH, index=False)
            
            # Create triples format for graph export
            triples = []
            for _, row in network_df.iterrows():
                triples.append({
                    'subject': row['musician'],
                    'predicate': row['role'],
                    'object': row['main_artist']
                })
            
            import pandas as pd
            triples_df = pd.DataFrame(triples)
            triples_df.to_csv(config.TRIPLES_CSV_PATH, index=False)
            
            if args.verbose:
                print(f"✅ CSV files saved:")
                print(f"   • {config.NETWORK_CSV_PATH}")
                print(f"   • {config.TRIPLES_CSV_PATH}")
        
        # Final summary
        if args.verbose:
            print()
            print("🎉 ANALYSIS COMPLETE!")
            print("=" * 50)
            
            # Get collaboration stats
            stats = get_collaboration_stats(network_df)
            print("📊 Collection Statistics:")
            print(f"   • Total connections: {stats['total_connections']}")
            print(f"   • Unique musicians: {stats['unique_musicians']}")
            print(f"   • Unique artists: {stats['unique_artists']}")
            print(f"   • Unique albums: {stats['unique_albums']}")
            print(f"   • Unique roles: {stats['unique_roles']}")
            print()
            print(f"🌟 Top collaborators:")
            print(f"   • Most collaborative musician: {stats['most_collaborative_musician']}")
            print(f"   • Most collaborative artist: {stats['most_collaborative_artist']}")
            print()
            print(f"🚀 Open '{args.output}' in your browser to explore!")
        else:
            print(f"✅ Analysis complete! Generated: {args.output}")
    
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 
