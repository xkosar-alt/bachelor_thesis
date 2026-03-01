#!/usr/bin/env python3
"""
Dataset Analysis and Visualization
This script provides tools for analyzing and visualizing the created dataset.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt


class DatasetAnalyzer:
    """Class for analyzing dataset statistics and quality."""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.stats = {}
    
    def load_annotations(self) -> List[Dict]:
        """Load annotation data."""
        annotations_file = self.dataset_path / 'annotations.json'
        if annotations_file.exists():
            with open(annotations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def compute_statistics(self):
        """Compute dataset statistics."""
        annotations = self.load_annotations()
        
        self.stats = {
            'total_images': len(annotations),
            'labels': {},
            'classes': set()
        }
        
        for ann in annotations:
            for label in ann.get('labels', []):
                self.stats['classes'].add(label)
                self.stats['labels'][label] = self.stats['labels'].get(label, 0) + 1
        
        self.stats['num_classes'] = len(self.stats['classes'])
        self.stats['classes'] = list(self.stats['classes'])
        
        return self.stats
    
    def print_summary(self):
        """Print dataset summary."""
        print("\n=== Dataset Summary ===")
        print(f"Total images: {self.stats.get('total_images', 0)}")
        print(f"Number of classes: {self.stats.get('num_classes', 0)}")
        print(f"\nClass distribution:")
        for label, count in self.stats.get('labels', {}).items():
            print(f"  {label}: {count}")
    
    def visualize_distribution(self, output_path: str = None):
        """Create visualization of class distribution."""
        if not self.stats.get('labels'):
            print("No data to visualize")
            return
        
        plt.figure(figsize=(10, 6))
        labels = list(self.stats['labels'].keys())
        counts = list(self.stats['labels'].values())
        
        plt.bar(labels, counts)
        plt.xlabel('Class')
        plt.ylabel('Count')
        plt.title('Dataset Class Distribution')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path)
            print(f"Visualization saved to {output_path}")
        else:
            plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Analyze agricultural dataset'
    )
    parser.add_argument(
        '--dataset',
        type=str,
        required=True,
        help='Path to dataset directory'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output path for visualization (optional)'
    )
    
    args = parser.parse_args()
    
    analyzer = DatasetAnalyzer(args.dataset)
    analyzer.compute_statistics()
    analyzer.print_summary()
    
    if args.output:
        analyzer.visualize_distribution(args.output)
    
    print("\nAnalysis completed!")


if __name__ == '__main__':
    main()
