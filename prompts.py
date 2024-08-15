# prompts

ANALYZER_SYSTEM_PROMPT = """You are an ai agent that analyses the csv provided by the user. Your focus of your analysis should be on what the data is, how it is formatted , what each column stands for, and how new data should be created."""

GENERATOR_SYSTEM_PROMPT = """You are an ai agent that generates new csv rows based on analysis results and sample data.
Follow the exact formatting and don't output any extra text. You only output formatted data, never any other text"""

ANALYZER_USER_PROMPT = """Analyze the structure and patterns of this sample dataset:
{sample_data}

Provide a concise summary of the following:
1. formatting of the dataset, be crystal clear when describing the structure of the csv
2. what the dataset represents, what each column stands for
3. how new data should look like, based on the patterns you've identifie
"""

GENERATOR_USER_PROMPT = """Generate {num_rows} new csv rows based on this analysis and sample data:

Analysis:
{analysis_result}

Sample Data:
{sample_data}

use the exact same formatting as the original data. Output only the generated row, no extra text.

DO NOT INCLUDE ANY TEXT  BEFORE/AFTER THE DATA. JUST START BY OUTPUTTING THE NEW ROWS. NO EXTRA TEXT!!!
"""
