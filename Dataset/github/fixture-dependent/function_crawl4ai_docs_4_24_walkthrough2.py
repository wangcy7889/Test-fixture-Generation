import os
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMExtractionStrategy

async def demo_input_formats():
    print('\n4. Input Format Handling Demo')
    print('---------------------------')
    dummy_html = '\n    <div class="job-posting" data-post-id="12345">\n        <header class="job-header">\n            <h1 class="job-title">Senior AI/ML Engineer</h1>\n            <div class="job-meta">\n                <span class="department">AI Research Division</span>\n                <span class="location" data-remote="hybrid">San Francisco (Hybrid)</span>\n            </div>\n            <div class="salary-info" data-currency="USD">\n                <span class="range">$150,000 - $220,000</span>\n                <span class="period">per year</span>\n            </div>\n        </header>\n\n        <section class="requirements">\n            <div class="technical-skills">\n                <h3>Technical Requirements</h3>\n                <ul class="required-skills">\n                    <li class="skill required" data-priority="must-have">\n                        5+ years experience in Machine Learning\n                    </li>\n                    <li class="skill required" data-priority="must-have">\n                        Proficiency in Python and PyTorch/TensorFlow\n                    </li>\n                    <li class="skill preferred" data-priority="nice-to-have">\n                        Experience with distributed training systems\n                    </li>\n                </ul>\n            </div>\n\n            <div class="soft-skills">\n                <h3>Professional Skills</h3>\n                <ul class="required-skills">\n                    <li class="skill required" data-priority="must-have">\n                        Strong problem-solving abilities\n                    </li>\n                    <li class="skill preferred" data-priority="nice-to-have">\n                        Experience leading technical teams\n                    </li>\n                </ul>\n            </div>\n        </section>\n\n        <section class="timeline">\n            <time class="deadline" datetime="2024-02-28">\n                Application Deadline: February 28, 2024\n            </time>\n        </section>\n\n        <footer class="contact-section">\n            <div class="hiring-manager">\n                <h4>Hiring Manager</h4>\n                <div class="contact-info">\n                    <span class="name">Dr. Sarah Chen</span>\n                    <span class="title">Director of AI Research</span>\n                    <span class="email">ai.hiring@example.com</span>\n                </div>\n            </div>\n            <div class="team-info">\n                <p>Join our team of 50+ researchers working on cutting-edge AI applications</p>\n            </div>\n        </footer>\n    </div>\n    '
    url = f'raw://{dummy_html}'
    from pydantic import BaseModel, Field
    from typing import List, Optional

    class JobRequirement(BaseModel):
        category: str = Field(description='Category of the requirement (e.g., Technical, Soft Skills)')
        items: List[str] = Field(description='List of specific requirements in this category')
        priority: str = Field(description='Priority level (Required/Preferred) based on the HTML class or context')

    class JobPosting(BaseModel):
        title: str = Field(description='Job title')
        department: str = Field(description='Department or team')
        location: str = Field(description='Job location, including remote options')
        salary_range: Optional[str] = Field(description='Salary range if specified')
        requirements: List[JobRequirement] = Field(description='Categorized job requirements')
        application_deadline: Optional[str] = Field(description='Application deadline if specified')
        contact_info: Optional[dict] = Field(description='Contact information from footer or contact section')
    markdown_strategy = LLMExtractionStrategy(provider='openai/gpt-4o', api_token=os.getenv('OPENAI_API_KEY'), schema=JobPosting.model_json_schema(), extraction_type='schema', instruction='\n        Extract job posting details into structured data. Focus on the visible text content \n        and organize requirements into categories.\n        ', input_format='markdown')
    html_strategy = LLMExtractionStrategy(provider='openai/gpt-4', api_token=os.getenv('OPENAI_API_KEY'), schema=JobPosting.model_json_schema(), extraction_type='schema', instruction="\n        Extract job posting details, using HTML structure to:\n        1. Identify requirement priorities from CSS classes (e.g., 'required' vs 'preferred')\n        2. Extract contact info from the page footer or dedicated contact section\n        3. Parse salary information from specially formatted elements\n        4. Determine application deadline from timestamp or date elements\n\n        Use HTML attributes and classes to enhance extraction accuracy.\n        ", input_format='html')
    async with AsyncWebCrawler() as crawler:
        markdown_config = CrawlerRunConfig(extraction_strategy=markdown_strategy)
        markdown_result = await crawler.arun(url=url, config=markdown_config)
        print('\nMarkdown-based Extraction Result:')
        items = json.loads(markdown_result.extracted_content)
        print(json.dumps(items, indent=2))
        html_config = CrawlerRunConfig(extraction_strategy=html_strategy)
        html_result = await crawler.arun(url=url, config=html_config)
        print('\nHTML-based Extraction Result:')
        items = json.loads(html_result.extracted_content)
        print(json.dumps(items, indent=2))