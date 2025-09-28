#!/usr/bin/env python3
"""
Migration guide for adding image_url column to access table
This script displays the migration SQL that needs to be run manually in Supabase
"""

import os
from pathlib import Path

def show_migration():
    """Display the migration SQL and instructions"""
    
    # Read the migration file
    migration_file = Path(__file__).parent / "migrations" / "001_add_image_url_column.sql"
    
    if not migration_file.exists():
        print(f"❌ Migration file not found: {migration_file}")
        return False
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    print("🚀 Migration: Add image_url column to access table")
    print("=" * 60)
    print()
    print("� Instructions:")
    print("1. Copy the SQL below")
    print("2. Go to your Supabase Dashboard")
    print("3. Open the SQL Editor")
    print("4. Paste and execute the SQL")
    print()
    print("📝 Migration SQL:")
    print("-" * 60)
    print(migration_sql)
    print("-" * 60)
    print()
    print("✅ After running this migration, your access table will:")
    print("• Have a new image_url column")
    print("• Automatically populate image_url when image_id is set")
    print("• Include image URLs in API responses")
    print("• Maintain data integrity with triggers")
    print()
    print("🎉 This will make the frontend integration much cleaner!")
    
    return True

if __name__ == "__main__":
    show_migration()