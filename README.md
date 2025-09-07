# CrewAI Financial Daily Summary

A comprehensive financial news aggregation and summarization system that automatically collects, processes, and distributes daily market summaries in multiple languages. This project implements a CrewAI-style agent workflow powered by **Groq's high-performance Language Processing Units (LPUs)** to create professional PDF reports with real-time financial data.

## 🚀 Features

- **High-Speed AI Processing**: Leverages Groq's LPUs for ultra-fast inference (100+ tokens/second)
- **Automated News Collection**: Fetches real-time US financial news using Serper and Tavily search APIs
- **AI-Powered Summarization**: Generates concise, professional summaries using Groq's language models
- **Multi-Language Support**: Translates summaries into Arabic, Hindi, and Hebrew
- **Professional PDF Generation**: Creates formatted PDF reports with embedded images
- **Telegram Integration**: Automatically sends reports to Telegram channels
- **Modular Agent Architecture**: Clean separation of concerns with dedicated agents for each task

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Requirements](#api-requirements)
- [Groq Integration](#groq-integration)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🛠 Installation

### Prerequisites

- Python 3.8 or higher
- API keys for required services (see [API Requirements](#api-requirements))

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Additional Dependencies

For the financial summary script specifically, you may need:

```bash
pip install crewai litellm requests python-telegram-bot==13.15 reportlab Pillow PyPDF2 groq langchain-groq
```

## ⚙️ Configuration

### Environment Variables

Set the following environment variables in your `.env` file or system environment:

```bash
# Groq Configuration (Primary LLM Provider)
GROQ_API_KEY=your_groq_api_key

# Search APIs (choose one or both)
SERPER_API_KEY=your_serper_api_key
TAVILY_API_KEY=your_tavily_api_key

# LLM Configuration (Fallback)
LITELLM_API_KEY=your_litellm_api_key
LLM_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini

# Telegram Integration (optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_telegram_channel_id
```

### API Keys Setup

1. **Groq API**: Sign up at [console.groq.com](https://console.groq.com) for high-speed LLM access
2. **Serper API**: Sign up at [serper.dev](https://serper.dev) for Google search API access
3. **Tavily API**: Get API key from [tavily.com](https://tavily.com) for enhanced search
4. **LiteLLM**: Configure with your preferred LLM provider (OpenAI, Anthropic, etc.) as fallback
5. **Telegram Bot**: Create a bot via [@BotFather](https://t.me/botfather) and get channel ID

## 🚀 Usage

### Basic Usage

Run the financial daily summary:

```bash
python crew_ai_financial_daily_summary.py --run
```

### Command Line Options

```bash
# Run the complete workflow
python crew_ai_financial_daily_summary.py --run

# Check configuration (without running)
python crew_ai_financial_daily_summary.py
```

### Programmatic Usage

```python
from crew_ai_financial_daily_summary import crewai_flow_run

# Run the complete workflow
success = crewai_flow_run()
if success:
    print("Daily summary generated successfully!")
```

## 🏗 Architecture

The system implements a multi-agent workflow inspired by CrewAI, optimized for Groq's high-speed processing:

### Agent Workflow

```mermaid
graph TD
    A[Search Agent] --> B[Summary Agent]
    B --> C[Image Selection]
    C --> D[Translation Agent]
    D --> E[PDF Generation]
    E --> F[Telegram Distribution]
    
    G[Groq LPU] --> B
    G --> D
```

### Agent Responsibilities

1. **Search Agent** (`search_agent_us_financial_news`)
   - Queries multiple search APIs (Serper, Tavily)
   - Deduplicates results
   - Focuses on US financial markets and recent news

2. **Summary Agent** (`summary_agent_generate`)
   - Processes search results using Groq's fast inference
   - Generates concise, professional summaries
   - Maintains factual accuracy

3. **Image Selection** (`select_images_from_results`)
   - Extracts relevant images from search results
   - Provides fallback placeholder images
   - Optimizes for PDF layout

4. **Translation Agent** (`translating_agent_translate`)
   - Translates summaries to multiple languages using Groq
   - Preserves formatting and structure
   - Supports Arabic, Hindi, and Hebrew

5. **PDF Generation** (`create_pdf`)
   - Creates professional PDF layouts
   - Embeds images and formatted text
   - Handles multi-language content

6. **Distribution Agent** (`send_to_telegram`)
   - Sends PDF reports to Telegram channels
   - Includes captions and metadata
   - Handles delivery confirmations

## 🔌 API Requirements

### Required APIs

| Service | Purpose | Free Tier | Documentation |
|---------|---------|-----------|---------------|
| **Groq** | **Primary LLM provider** | **14,400 requests/day** | [console.groq.com](https://console.groq.com) |
| Serper | Web search | 2,500 queries/month | [serper.dev](https://serper.dev) |

### Optional APIs

| Service | Purpose | Free Tier | Documentation |
|---------|---------|-----------|---------------|
| Tavily | Enhanced search | 1,000 queries/month | [tavily.com](https://tavily.com) |
| LiteLLM | Fallback LLM access | Varies by provider | [litellm.ai](https://litellm.ai) |
| Telegram Bot API | Distribution | Free | [core.telegram.org](https://core.telegram.org/bots) |

## ⚡ Groq Integration

### Why Groq?

- **Ultra-Fast Inference**: 100+ tokens per second processing speed
- **Cost-Effective**: Generous free tier with 14,400 requests per day
- **High-Quality Models**: Access to Llama 3, Mixtral, and other state-of-the-art models
- **Low Latency**: Optimized for real-time applications

### Current Groq Models

**⚠️ Important**: The `llama3-8b-8192` model has been decommissioned. Use these current models:

| Model | Context Length | Best For | Speed |
|-------|----------------|----------|-------|
| `llama-3.3-70b-versatile` | 8,192 tokens | High-quality reasoning | Fast |
| `llama3-70b-8192` | 8,192 tokens | **DEPRECATED** | N/A |
| `llama3-8b-8192` | 8,192 tokens | **DEPRECATED** | N/A |
| `mixtral-8x7b-32768` | 32,768 tokens | Long context, multilingual | Very Fast |
| `gemma-7b-it` | 8,192 tokens | General purpose | Very Fast |

### Groq Configuration Example

```python
from langchain_groq import ChatGroq

# Update your agent.py to use current models
LLM = ChatGroq(
    model="llama-3.3-70b-versatile",  # or "mixtral-8x7b-32768"
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)
```

### Model Migration Guide

If you're currently using the deprecated `llama3-8b-8192` model:

1. **Update your code**:
   ```python
   # Old (deprecated)
   LLM = ChatGroq(model="llama3-8b-8192")
   
   # New (recommended)
   LLM = ChatGroq(model="llama-3.3-70b-versatile")  # Better quality
   # or
   LLM = ChatGroq(model="mixtral-8x7b-32768")  # Longer context
   ```

2. **Update environment variables**:
   ```bash
   # Add to your .env file
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

## 📄 Output

### Generated Files

- **PDF Report**: `daily_summary_YYYYMMDD.pdf`
  - English summary with market analysis
  - Translated versions in Arabic, Hindi, Hebrew
  - Embedded financial charts and images
  - Professional formatting

### Sample Output Structure

```
daily_summary_20241201.pdf
├── English Summary
│   ├── Key market movements
│   ├── Trading activity highlights
│   └── Market drivers analysis
├── Arabic Summary (العربية)
├── Hindi Summary (हिन्दी)
├── Hebrew Summary (עברית)
└── Financial Charts & Images
```

### Telegram Distribution

When configured, reports are automatically sent to your Telegram channel with:
- PDF attachment
- Descriptive caption
- Date stamp
- Delivery confirmation

## 🔧 Customization

### Adding New Languages

To add support for additional languages:

1. Update the `LANGUAGE_CODES` dictionary:
```python
LANGUAGE_CODES = {
    "arabic": "ar", 
    "hindi": "hi", 
    "hebrew": "he",
    "spanish": "es",  # Add new language
    "french": "fr"    # Add new language
}
```

2. Modify the translation loop in `crewai_flow_run()`:
```python
for lang in ["arabic", "hindi", "hebrew", "spanish", "french"]:
    translations[lang] = translating_agent_translate(summary_en, lang)
```

### Customizing Search Queries

Modify the search query in `search_agent_us_financial_news()`:

```python
query = "Your custom financial news query"
```

### PDF Layout Customization

Adjust the PDF generation in `create_pdf()`:
- Change page size and margins
- Modify font styles and sizes
- Adjust image placement and sizing
- Customize section headers

## 🐛 Troubleshooting

### Common Issues

1. **Groq Model Decommissioned Error**
   ```
   Error: The model `llama3-8b-8192` has been decommissioned
   ```
   **Solution**: Update to a current model:
   ```python
   # In agent.py, change:
   LLM = ChatGroq(model="llama-3.3-70b-versatile")  # or mixtral-8x7b-32768
   ```

2. **API Key Errors**
   - Verify all API keys are correctly set
   - Check API quotas and billing status
   - Ensure proper environment variable loading

3. **Search Failures**
   - The system automatically falls back between Serper and Tavily
   - Check internet connectivity
   - Verify search API endpoints are accessible

4. **LLM Errors**
   - Confirm Groq API key is valid
   - Check model availability and pricing
   - Verify API rate limits (14,400 requests/day free tier)

5. **PDF Generation Issues**
   - Ensure sufficient disk space
   - Check image URL accessibility
   - Verify PIL/Pillow installation

6. **Telegram Delivery**
   - Verify bot token and channel ID
   - Check bot permissions in the channel
   - Ensure file size limits are respected

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

- **Use Groq's fastest models** for real-time applications
- **Batch requests** when possible to maximize throughput
- **Monitor API usage** to stay within free tier limits
- **Cache results** for repeated queries

## 📊 Performance

### Typical Runtime (with Groq)

- **Search Phase**: 10-30 seconds
- **Summary Generation**: 5-15 seconds (Groq's speed advantage)
- **Translation**: 15-45 seconds (3 languages, Groq accelerated)
- **PDF Creation**: 5-15 seconds
- **Telegram Upload**: 5-20 seconds

**Total Runtime**: 40 seconds - 2.5 minutes (significantly faster with Groq)

### Resource Usage

- **Memory**: ~100-200MB peak usage
- **Network**: ~10-50MB data transfer
- **Storage**: ~1-5MB per generated PDF
- **API Calls**: ~10-20 Groq requests per run

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
git clone <repository-url>
cd CrewAI-Financial-Daily-Summary
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for providing ultra-fast Language Processing Units
- [CrewAI](https://github.com/joaomdmoura/crewAI) for the agent workflow inspiration
- [LiteLLM](https://github.com/BerriAI/litellm) for LLM abstraction
- [Serper](https://serper.dev) and [Tavily](https://tavily.com) for search capabilities
- [ReportLab](https://www.reportlab.com) for PDF generation

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the troubleshooting section
- Review [Groq's documentation](https://console.groq.com/docs)
- Review API documentation for external services

---

**Note**: This implementation is optimized for Groq's high-speed processing. You must configure your own API keys and may need to adapt the code for your specific requirements. The deprecated `llama3-8b-8192` model should be replaced with current Groq models for optimal performance.