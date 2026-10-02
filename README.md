# Developer Skills Ecosystem Analysis

A multi-platform analysis of technology skills clustering and role prediction using Stack Overflow survey data and GitHub profile data.

**Author:** Krishna Kishore Madathingal

## Research Overview

This research examines how technology skills form natural communities and enable role prediction across different developer specializations. Using network analysis, text mining, and machine learning on 15,320 Stack Overflow survey responses and 303 GitHub profiles, the study reveals:

- **4 distinct technology communities** with high network density (0.69)
- **81.5% accuracy** in predicting developer roles from technology stacks
- **Systematic linguistic patterns** in how developers describe their expertise

## Research Questions

**RQ1 (Network Analysis):** How do technology skills cluster into natural communities based on co-occurrence patterns?

**RQ2 (Text Analysis):** How do developers linguistically describe their expertise in profile descriptions?

**RQ3 (Machine Learning):** Can developer roles be accurately predicted from technology stack compositions?

## Repository Structure

```
developer-skills-ecosystem/
├── data/
│   ├── stackoverflow_data.zip                 # Contains stackoverflow_survey.csv (89,184 raw responses)
│   ├── stackoverflow_data_cleaned.zip         # Contains stackoverflow_survey_cleaned.csv (15,320 filtered)
│   └── github_profiles.csv                    # GitHub user profiles (303 users)
├── code/
│   ├── data_collection.py                     # GitHub API collection script
│   └── developer_skills_analysis.ipynb        # Complete analysis notebook
├── figures/
│   ├── confusion_matrix_normalized_*.png      # Normalized confusion matrix
│   ├── confusion_matrix_roles.png             # Raw confusion matrix
│   ├── data_overview.png                      # Role distribution & top technologies
│   ├── feature_importance_roles.png           # Top predictive features
│   ├── platform_comparison.png                # GitHub vs Stack Overflow comparison
│   ├── role_confusion_pairs.png               # Role confusion analysis
│   ├── technology_network_focused.png         # Network visualization (focused)
│   ├── technology_network_hierarchical*.png   # Network visualization (hierarchical)
│   └── tfidf_github_bios.png                  # TF-IDF analysis of bios
├── output/
│   ├── technology_centrality.csv              # Network centrality measures
│   └── lda_visualization.html                 # Interactive topic modeling output
├── requirements.txt                           # Python dependencies
├── developer_skills_ecosystem_report.pdf      # Full research report
└── README.md
```

## Methodology

### Data Sources

**Stack Overflow Developer Survey 2024**
- Raw sample: 89,184 responses
- Filtered sample: 15,320 responses (after quality control and role filtering)
- Source: https://insights.stackoverflow.com/survey
- Collection: May 2024 (official survey data)
- Usage: Network analysis (RQ1), Machine learning (RQ3)

**GitHub API**
- Sample: 303 user profiles, ~9,090 repositories analyzed
- Collection: November 2025 (automated API calls using GitHub REST API v3)
- Usage: Text analysis (RQ2), Cross-platform validation

### Analysis Pipeline

1. **Network Analysis** (Stack Overflow data)
   - Technology co-occurrence network construction (185 nodes, 11,765 edges)
   - Louvain community detection (4 communities identified)
   - Centrality analysis (degree, betweenness, eigenvector)
   - Network density: 0.69 (highly interconnected ecosystem)

2. **Text Analysis** (GitHub data)
   - TF-IDF term extraction from profile bios (289 bios with text, 95.4% completion rate)
   - Latent Dirichlet Allocation (LDA) topic modeling (7 topics)

3. **Machine Learning** (Stack Overflow data)
   - Binary feature encoding (151 technology features + years of experience)
   - Multi-class classification (5 roles: Backend, Data Scientist, DevOps, Frontend, QA)
   - Models: Random Forest, Logistic Regression, Naive Bayes
   - Dataset: 15,247 observations (12,197 train, 3,050 test)

## Quick Start

### Prerequisites

- Python 3.12 or higher
- Jupyter Notebook or JupyterLab
- ~8GB RAM
- (Optional) GitHub personal access token for fresh data collection

### Installation

```bash
# Clone the repository
git clone https://github.com/madathingalkrishnak/developer-skills-ecosystem.git
cd developer-skills-ecosystem

# Install dependencies
pip install -r requirements.txt

# Extract data files
unzip data/stackoverflow_data.zip -d data/
unzip data/stackoverflow_data_cleaned.zip -d data/
```

### Running the Analysis

```bash
# Open the Jupyter notebook
jupyter notebook code/developer_skills_analysis.ipynb
```

Run all cells sequentially from top to bottom. The complete analysis takes approximately 15-20 minutes on a standard laptop.

### Collecting Fresh GitHub Data (Optional)

```bash
# Set your GitHub token
export GITHUB_TOKEN='your_github_token_here'

# Run the collection script
python code/data_collection.py
```

## Key Findings

### Technology Communities

Four distinct communities identified:
1. **Web Development** (48 technologies): JavaScript, TypeScript, React, Vue, Angular, Node.js
2. **Specialized/Emerging** (26 technologies): Mobile and emerging technology cluster
3. **Data Science/Analytics** (50 technologies): Python, R, Jupyter, TensorFlow, scikit-learn, pandas
4. **Backend/DevOps/Enterprise** (61 technologies): Java, C#, Docker, Kubernetes, databases, enterprise tools

### Network Characteristics

- **185 nodes** (technologies analyzed)
- **11,765 edges** (co-occurrence relationships)
- **Network density: 0.69** (highly interconnected -- developers use broad technology stacks)
- **Mean degree: 127.2** (average technology co-occurs with 127 others)

### Role Prediction Performance

| Role | Precision | Recall | F1-Score | Dataset % |
|------|-----------|--------|----------|-----------|
| Data Scientist | 81.6% | 93.4% | 87.1% | 6.5% |
| DevOps Engineer | 84.5% | 80.1% | 82.2% | 6.5% |
| Backend Developer | 80.8% | 70.6% | 75.3% | 62.8% |
| Frontend Developer | 56.7% | 19.2% | 28.7% | 21.1% |
| QA Engineer | 66.7% | 6.2% | 11.3% | 3.2% |

**Overall Accuracy:** 81.5% (vs. 20% random baseline, 62.8% majority baseline)

### Top Predictive Technologies

1. Groovy (2.01)
2. R (1.98)
3. Python (1.96)
4. Go (1.95)
5. HTML/CSS (1.86)
6. JavaScript (1.84)
7. Scikit-Learn (1.79)
8. React (1.71)
9. Redis (1.64)
10. SQL (1.43)

Years of professional experience ranked 151st out of 151 features, indicating role differentiation is driven by technology choices rather than tenure.

## Dependencies

See `requirements.txt` for complete list. Major dependencies:

- pandas, numpy -- Data manipulation
- matplotlib, seaborn -- Visualization
- networkx, python-louvain -- Network analysis and community detection
- scikit-learn -- Machine learning and NLP
- requests -- API calls

## Key Takeaways

1. **Technology ecosystems are highly interconnected** -- Network density of 0.69 suggests modern developers work with broad, overlapping technology stacks
2. **Role boundaries are partially fluid** -- High confusion between Backend and Frontend roles, but Data Scientists show distinctive technology profiles
3. **Class imbalance matters** -- Performance varies significantly by role representation in the dataset
4. **Experience doesn't predict roles** -- Role specialization is determined by technology choices, not years of experience
5. **Platform consistency validated** -- Core languages (JavaScript, Python, Java) maintain similar prominence across Stack Overflow and GitHub