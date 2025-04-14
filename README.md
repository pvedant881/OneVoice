# Smart Business Chatbot

A Flask-based chatbot that uses the Gemini API to answer questions based on local data files and website content.

## Prerequisites

- Python 3.8+
- Vercel CLI (for deployment)
- GitHub account

## Setup

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variable: `export GEMINI_API_KEY=your_key` (or set in Vercel dashboard).
4. Pre-crawl websites and save results to `data/crawled_data.json` using `crawlers/website_crawler.py`.
5. Deploy to Vercel using `vercel` or via the Vercel dashboard.

## Deployment

- Push code to GitHub.
- Link repository to Vercel.
- Configure `vercel.json` and environment variables in Vercel.

## Notes

- Local data files should be in the `data/` folder.
- Web crawling is pre-processed to avoid runtime limits on Vercel.