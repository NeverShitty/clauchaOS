from setuptools import setup, find_packages

setup(
    name="cloude-memory-system-v3",
    version="3.0.0",
    description="Enhanced Cloude Memory System with OpenAI Assistants Integration",
    author="NeverShitty",
    author_email="cloude@nevershitty.com",
    url="https://github.com/NeverShitty/clauchaOS",
    license="Commercial",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.25.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "tiktoken>=0.5.0",
        "schedule>=1.2.0",
        "python-dotenv>=1.0.0",
        "reportlab>=4.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "pandas>=2.0.0",
        "flask>=2.3.0",
        "flask-socketio>=5.3.0",
        "stripe>=6.0.0",
        "boto3>=1.28.0",
        "cryptography>=41.0.0",
        "bcrypt>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "jupyter>=1.0.0",
            "ipykernel>=6.25.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "cloude-memory=src.cloude_vector_memory_v3_enhanced:main",
            "cloude-insights=src.cloude_automated_insights_generator:main",
            "cloude-monitor=src.cloude_memory_monitoring_dashboard:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
    ],
)
EOF < /dev/null