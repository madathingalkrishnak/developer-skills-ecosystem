"""
Data Collection Script for Developer Skills Analysis
Stack Overflow Survey + GitHub API

This script collects:
1. Stack Overflow Annual Developer Survey data (download manually)
2. GitHub user profiles via API (automated)

Author: Krishna Kishore Madathingal
Date: December 2025
"""

import pandas as pd
import requests
import time
import json
from datetime import datetime
from typing import List, Dict
import os

# ============================================================================
# PART 1: STACK OVERFLOW SURVEY DATA
# ============================================================================

def download_stackoverflow_instructions():
    """
    Instructions for downloading Stack Overflow survey data.
    This must be done manually but takes only 5 minutes.
    """
    print("=" * 80)
    print("STACK OVERFLOW SURVEY DATA COLLECTION")
    print("=" * 80)
    print("\nSTEP 1: Download the data manually:")
    print("1. Go to: https://insights.stackoverflow.com/survey")
    print("2. Find the latest year (2024 or 2023)")
    print("3. Click 'Download Full Data Set (CSV)'")
    print("4. Save as: 'stackoverflow_survey.csv' in this directory")
    print("\nSTEP 2: After downloading, run this script again")
    print("=" * 80)

def load_stackoverflow_data(filepath='stackoverflow_survey.csv'):
    """
    Load and preprocess Stack Overflow survey data.
    """
    try:
        print(f"\nLoading Stack Overflow survey data from {filepath}...")
        df = pd.read_csv(filepath, low_memory=False)
        print(f"✓ Loaded {len(df)} survey responses")
        print(f"✓ Columns available: {df.shape[1]}")
        
        # Show relevant columns
        relevant_cols = [col for col in df.columns if any(
            keyword in col.lower() 
            for keyword in ['devtype', 'languageworkedwith', 'databaseworkedwith', 
                           'platformworkedwith', 'webframeworkworkedwith','misctechworkedwith',
                           'toolstechworkedwith', 'aisearchworkedwith','yearscodepro', 'edlevel']
        )]
        
        if relevant_cols:
            print(f"\n✓ Relevant columns for analysis:")
            for col in relevant_cols[:10]:  # Show first 10
                print(f"  - {col}")
        
        return df
    
    except FileNotFoundError:
        print(f"\n✗ ERROR: {filepath} not found!")
        download_stackoverflow_instructions()
        return None

def preprocess_stackoverflow_data(df):
    """
    Clean and prepare Stack Overflow data for analysis.
    """
    print("\nPreprocessing Stack Overflow data...")
    
    # Common column names (vary by year, adjust as needed)
    # For 2023 survey
    role_col = 'DevType'  # or 'MainBranch' in some years
    lang_col = 'LanguageHaveWorkedWith'  # or 'LanguageWorkedWith'
    
    # Check which columns exist
    if role_col not in df.columns:
        # Try alternative names
        possible_role_cols = [col for col in df.columns if 'dev' in col.lower() and 'type' in col.lower()]
        if possible_role_cols:
            role_col = possible_role_cols[0]
            print(f"Using role column: {role_col}")
    
    if lang_col not in df.columns:
        possible_lang_cols = [col for col in df.columns if 'language' in col.lower()]
        if possible_lang_cols:
            lang_col = possible_lang_cols[0]
            print(f"Using language column: {lang_col}")
    
    # Filter to respondents with both role and skills data
    df_clean = df.dropna(subset=[role_col, lang_col]).copy()
    
    print(f"✓ Cleaned dataset: {len(df_clean)} responses")
    
    return df_clean, role_col, lang_col

# ============================================================================
# PART 2: GITHUB API DATA COLLECTION
# ============================================================================

class GitHubDataCollector:
    """
    Collect GitHub user profiles using the official GitHub API.
    """
    
    def __init__(self, access_token=None):
        """
        Initialize with GitHub personal access token.
        
        Get token from: https://github.com/settings/tokens
        Permissions needed: public_repo, read:user
        """
        self.access_token = access_token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if access_token:
            self.headers['Authorization'] = f'token {access_token}'
        
        self.base_url = 'https://api.github.com'
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None
    
    def check_rate_limit(self):
        """Check GitHub API rate limit."""
        url = f'{self.base_url}/rate_limit'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            self.rate_limit_remaining = data['resources']['core']['remaining']
            self.rate_limit_reset = data['resources']['core']['reset']
            
            print(f"Rate limit: {self.rate_limit_remaining} requests remaining")
            
            if self.rate_limit_remaining < 10:
                reset_time = datetime.fromtimestamp(self.rate_limit_reset)
                print(f"⚠ Warning: Rate limit low. Resets at {reset_time}")
                return False
        
        return True
    
    def search_users(self, query: str, max_results: int = 100) -> List[str]:
        """
        Search for GitHub users matching criteria.
        
        Args:
            query: Search query (e.g., "location:sanfrancisco repos:>5")
            max_results: Maximum number of users to return
        
        Returns:
            List of usernames
        """
        print(f"\nSearching GitHub users: {query}")
        usernames = []
        page = 1
        per_page = 30  # GitHub max per page
        
        while len(usernames) < max_results:
            url = f'{self.base_url}/search/users'
            params = {
                'q': query,
                'per_page': per_page,
                'page': page
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                if not items:
                    print(f"No more results found")
                    break
                
                for item in items:
                    usernames.append(item['login'])
                    if len(usernames) >= max_results:
                        break
                
                print(f"  Found {len(usernames)} users so far...")
                page += 1
                time.sleep(2)  # Rate limiting
            
            elif response.status_code == 403:
                print("Rate limit exceeded. Waiting...")
                time.sleep(60)
            
            else:
                print(f"Error: {response.status_code}")
                break
        
        print(f"✓ Total users found: {len(usernames)}")
        return usernames[:max_results]
    
    def get_user_profile(self, username: str) -> Dict:
        """
        Get detailed profile for a GitHub user.
        """
        url = f'{self.base_url}/users/{username}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting {username}: {response.status_code}")
            return None
    
    def get_user_repos(self, username: str, max_repos: int = 30) -> List[Dict]:
        """
        Get user's repositories.
        """
        url = f'{self.base_url}/users/{username}/repos'
        params = {
            'sort': 'updated',
            'per_page': max_repos
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
    
    def get_repo_languages(self, username: str, repo_name: str) -> Dict:
        """
        Get programming languages used in a repository.
        """
        url = f'{self.base_url}/repos/{username}/{repo_name}/languages'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    
    def collect_user_data(self, username: str) -> Dict:
        """
        Collect comprehensive data for a single user.
        """
        print(f"  Collecting data for {username}...", end='')
        
        # Get profile
        profile = self.get_user_profile(username)
        if not profile:
            print(" ✗ Failed")
            return None
        
        # Get repositories
        repos = self.get_user_repos(username, max_repos=30)
        
        # Aggregate languages across all repos
        all_languages = {}
        repo_topics = []
        
        for repo in repos[:10]:  # Check top 10 repos
            # Languages
            languages = self.get_repo_languages(username, repo['name'])
            for lang, bytes_code in languages.items():
                all_languages[lang] = all_languages.get(lang, 0) + bytes_code
            
            # Topics/tags
            if 'topics' in repo and repo['topics']:
                repo_topics.extend(repo['topics'])
            
            time.sleep(0.5)  # Rate limiting
        
        # Prepare output
        user_data = {
            'username': username,
            'name': profile.get('name', ''),
            'bio': profile.get('bio', ''),
            'company': profile.get('company', ''),
            'location': profile.get('location', ''),
            'public_repos': profile.get('public_repos', 0),
            'followers': profile.get('followers', 0),
            'following': profile.get('following', 0),
            'created_at': profile.get('created_at', ''),
            'languages': ','.join(all_languages.keys()) if all_languages else '',
            'top_language': max(all_languages.items(), key=lambda x: x[1])[0] if all_languages else '',
            'topics': ','.join(set(repo_topics)) if repo_topics else '',
            'num_languages': len(all_languages)
        }
        
        print(" ✓")
        return user_data
    
    def collect_batch(self, search_queries: List[str], users_per_query: int = 50) -> pd.DataFrame:
        """
        Collect data for multiple search queries.
        
        Args:
            search_queries: List of search strings
            users_per_query: Number of users to collect per query
        
        Returns:
            DataFrame with all collected user data
        """
        all_users_data = []
        
        for query in search_queries:
            print(f"\n{'='*80}")
            print(f"Query: {query}")
            print('='*80)
            
            # Search users
            usernames = self.search_users(query, max_results=users_per_query)
            
            # Collect data for each user
            for username in usernames:
                user_data = self.collect_user_data(username)
                if user_data:
                    all_users_data.append(user_data)
                
                time.sleep(1)  # Rate limiting
                
                # Check rate limit periodically
                if len(all_users_data) % 20 == 0:
                    self.check_rate_limit()
        
        df = pd.DataFrame(all_users_data)
        print(f"\n{'='*80}")
        print(f"✓ Total users collected: {len(df)}")
        print('='*80)
        
        return df

# ============================================================================
# MAIN COLLECTION FUNCTION
# ============================================================================

def main():
    """
    Main data collection workflow.
    """
    print("\n" + "="*80)
    print("DEVELOPER SKILLS ANALYSIS - DATA COLLECTION")
    print("="*80)
    
    # ========================================================================
    # STEP 1: Stack Overflow Survey Data
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 1: STACK OVERFLOW SURVEY DATA")
    print("="*80)
    
    # Try to load existing data
    so_df = load_stackoverflow_data()
    
    if so_df is None:
        print("\n⚠ Please download Stack Overflow survey data first")
        print("Then run this script again")
        return
    
    # Preprocess
    so_df_clean, role_col, lang_col = preprocess_stackoverflow_data(so_df)
    
    # Save cleaned version
    so_df_clean.to_csv('stackoverflow_survey_cleaned.csv', index=False)
    print(f"✓ Saved cleaned data to stackoverflow_survey_cleaned.csv")
    
    # ========================================================================
    # STEP 2: GitHub API Data Collection
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 2: GITHUB API DATA COLLECTION")
    print("="*80)
    
    # Check for GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("\n⚠ GitHub token not found!")
        print("\nTo get a token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Select scopes: public_repo, read:user")
        print("4. Copy the token")
        print("\nThen set it:")
        print("  export GITHUB_TOKEN='your_token_here'")
        print("\nOr hardcode it in the script (not recommended for sharing)")
        
        # Allow user to input token
        token_input = input("\nPaste your GitHub token (or press Enter to skip): ").strip()
        if token_input:
            github_token = token_input
        else:
            print("\nSkipping GitHub collection for now.")
            print("You can run this script again later with a token.")
            return
    
    # Initialize collector
    collector = GitHubDataCollector(access_token=github_token)
    
    # Check rate limit
    if not collector.check_rate_limit():
        print("Rate limit too low. Try again later.")
        return
    
    # Define search queries targeting different developer roles
    search_queries = [
        # Data Scientists
        'data scientist location:sanfrancisco repos:>5',
        'data scientist location:seattle repos:>5',
        
        # Software Engineers
        'software engineer location:sanfrancisco repos:>10',
        'software engineer location:seattle repos:>10',
        
        # Web Developers
        'web developer location:austin repos:>5',
        'full stack location:boston repos:>5',
        
        # DevOps
        'devops location:sanfrancisco repos:>5',
        
        # Additional diverse searches
        'machine learning repos:>20 followers:>50',
        'frontend developer repos:>10'
    ]
    
    print(f"\nWill collect ~50 users per query")
    print(f"Total queries: {len(search_queries)}")
    print(f"Expected total users: ~{len(search_queries) * 50}")
    
    proceed = input("\nProceed with collection? (yes/no): ").strip().lower()
    
    if proceed != 'yes':
        print("Collection cancelled.")
        return
    
    # Collect data
    github_df = collector.collect_batch(search_queries, users_per_query=50)
    
    # Save to CSV
    github_df.to_csv('github_profiles.csv', index=False)
    print(f"\n✓ Saved GitHub data to github_profiles.csv")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("DATA COLLECTION COMPLETE!")
    print("="*80)
    print(f"\n✓ Stack Overflow: {len(so_df_clean)} responses")
    print(f"✓ GitHub: {len(github_df)} profiles")
    print(f"\nFiles created:")
    print("  - stackoverflow_survey_cleaned.csv")
    print("  - github_profiles.csv")
    print("\nNext step: Run the analysis notebook!")
    print("="*80)

if __name__ == '__main__':
    main()
