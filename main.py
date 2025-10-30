import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, LLMConfig, BrowserConfig
from crawl4ai import LLMExtractionStrategy
from pydantic import BaseModel, Field


class Features(BaseModel):
    statistics_addition: float =  Field(..., description="The proportion of sentences that contain numerical data, percentages, or cited figures, with value in the range of 0 to 1")
    quotation_addition: float  = Field(..., description="The proportion of sentences that contain direct quotations from sources, with value in the range of 0 to 1")
    cite_sources: float = Field(..., description="The proportion of sentences that cite sources, with value in the range of 0 to 1")
    high_fluency: float = Field(..., description="The proportion of sentences that are written in a high-fluency style, with value in the range of 0 to 1")
    accurate_terminology: float = Field(..., description="The proportion of sentences that use accurate terminology, with value in the range of 0 to 1")
    non_manipulative_tone: float = Field(..., description="The proportion of sentences that are written in a non-manipulative tone, with value in the range of 0 to 1")


class Statistics(BaseModel):
    total_number_of_sentences: int = Field(..., description="The total number of sentences in the text")
    total_sentences_with_statistics: int = Field(..., description="The total number of sentences that contain numerical data, percentages, or cited figures")



async def extract_structured_data(provider: str, api_token: str = None):

    print(f"Extracting structured data from url using {provider}...")


    browser_config = BrowserConfig(headless=True)

    extra_arguments = {
        "temperature": 0,
        "top_p": 0.9,
        "max_tokens": 1000,

    }

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=LLMExtractionStrategy(
            llm_config=LLMConfig(provider=provider, api_token=api_token),
            schema=Features.model_json_schema(),
            extraction_type="schema",
            input_format="markdown",
            extra_arguments=extra_arguments,
            instructions="From the crawled text, extract all the text and deduce the features that I described in the schema.",
        )
    )


    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url="https://www.aljazeera.com/news/2021/11/1/modi-india-to-hit-net-zero-climate-target-by-2070", config=crawler_config, excluded_tags=True)
        print(result.extracted_content)





async def simple_crawl(url: str):
    browser_config = BrowserConfig(headless=True)
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url)
        print(result)


if __name__ == "__main__":
    # asyncio.run(simple_crawl(url="https://www.conning.com/about-us/insights/equity-market-outlook-column-2025#:~:text=From%20Q2%202023%20%2D%20estimated%20Q2,a%20paltry%206%25%20on%20average."))
    asyncio.run(extract_structured_data(provider="ollama/gemma3"))