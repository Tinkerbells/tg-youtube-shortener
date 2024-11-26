from yandex_gpt import YandexGPT

async def summarize_text_async(api_key, text, model='gpt4', max_tokens=1000):
    """
    Asynchronously summarize text using YandexGPT library.
    """
    # Initialize YandexGPT client
    yandex_gpt = YandexGPT(api_key)

    # Prepare the prompt
    prompt = f"Summarize the following text:\n\n{text}"

    # Request asynchronous completion
    response = await yandex_gpt.get_async_completion(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=0
    )

    # Extract and return the response text
    return response.get("choices", [{}])[0].get("text", "").strip()

# Example usage
if __name__ == "__main__":
    import asyncio

    api_key = "мне нужен ваш api"

    text_to_summarize = (
        ...
    )

    async def main():
        try:
            summary = await summarize_text_async(api_key, text_to_summarize)
            print("Summary:", summary)
        except Exception as e:
            print("An error occurred:", e)

    asyncio.run(main())