import argparse

from playwright.sync_api import sync_playwright


def main(
    url: str, selector: str, timeout: float, content_type: str, headless: bool
) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url)
        while True:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    for index, element in enumerate(elements):
                        print(element)
                        print(f"Element {index + 1}:")
                        a_tag = element.query_selector("xpath=..")
                        if a_tag is not None:
                            href = a_tag.get_attribute("href")
                            print(href)
                        if content_type == "text":
                            print(element.text_content())
                        elif content_type == "html":
                            print(element.inner_html())
                        else:
                            print(
                                "Invalid content type. Please choose 'text' or 'html'."
                            )
                        print()  # Add a blank line between elements
                else:
                    print("Selector found no content")
                selector = input("\nTry new selector (q to quit): ")
                if selector.lower() == "q":
                    break
            except Exception as e:
                print(f"Error: {str(e)}")
                selector = input("\nTry new selector (q to quit): ")
                if selector.lower() == "q":
                    break
        browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test a selector on a webpage using Playwright."
    )
    parser.add_argument("url", type=str, help="The URL of the webpage to test.")
    parser.add_argument("selector", type=str, help="The selector to test.")
    parser.add_argument(
        "--timeout",
        type=float,
        default=3,
        help="The timeout (in seconds) for the selector to appear.",
    )
    parser.add_argument(
        "--content-type",
        type=str,
        default="text",
        choices=["text", "html"],
        help="The type of content to display (text or html).",
    )
    parser.add_argument(
        "--headless",
        type=bool,
        default=True,
        choices=[True, False],
        help="Whether or not the browser runs in headless mode or not",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.url, args.selector, args.timeout, args.content_type, args.headless)
