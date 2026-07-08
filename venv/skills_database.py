# skills_database.py
# Comprehensive list of tech skills organized by category

SKILLS_DATABASE = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "ruby", 
        "go", "rust", "kotlin", "swift", "php", "scala", "r", "matlab",
        "perl", "dart", "lua", "bash", "shell"
    ],
    "Web Development": [
        "html", "css", "react", "angular", "vue", "nodejs", "express",
        "django", "flask", "fastapi", "spring", "laravel", "rails",
        "nextjs", "svelte", "bootstrap", "tailwind", "jquery", "sass"
    ],
    "Data Science & ML": [
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
        "seaborn", "nlp", "computer vision", "opencv", "spacy",
        "huggingface", "transformers", "xgboost", "lightgbm"
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
        "oracle", "sqlite", "dynamodb", "firebase", "elasticsearch",
        "neo4j", "mariadb", "snowflake"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
        "terraform", "ansible", "git", "github", "gitlab", "cicd",
        "linux", "nginx", "apache", "heroku", "vercel", "netlify"
    ],
    "Data Engineering": [
        "spark", "hadoop", "kafka", "airflow", "etl", "data warehouse",
        "databricks", "snowflake", "bigquery", "redshift", "tableau",
        "power bi", "looker", "dbt"
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "analytical", "creative", "collaboration", "agile", "scrum",
        "project management"
    ],
    "Tools & Others": [
        "jira", "confluence", "slack", "figma", "postman", "vscode",
        "intellij", "eclipse", "notion", "trello"
    ]
}

def get_all_skills():
    """Returns a flat list of all skills."""
    all_skills = []
    for category, skills in SKILLS_DATABASE.items():
        all_skills.extend(skills)
    return all_skills

def get_skill_category(skill):
    """Returns the category of a given skill."""
    for category, skills in SKILLS_DATABASE.items():
        if skill.lower() in skills:
            return category
    return "Other"