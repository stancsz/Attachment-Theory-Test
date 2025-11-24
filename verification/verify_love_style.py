
from playwright.sync_api import sync_playwright, expect

def verify_love_style_test():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 1. Go to app
            page.goto("http://localhost:5173")

            # 2. Check if new Love Style button exists and click it
            love_style_btn = page.get_by_role("button", name="Start Color Wheel Test (Self)")
            if not love_style_btn.is_visible():
                # It might be under "开始色轮测试 (仅自测)" if default lang is zh-CN
                love_style_btn = page.get_by_role("button", name="开始色轮测试 (仅自测)")

            expect(love_style_btn).to_be_visible()

            # Take screenshot of Intro screen with new button
            page.screenshot(path="verification/intro_screen.png")
            print("Intro screen captured.")

            # 3. Start the test
            love_style_btn.click()

            # 4. Verify first question is from Love Style set (e.g., mentions physical attraction or love at first sight)
            # "我相信一见钟情" or "I believe in love at first sight"
            first_q = page.get_by_role("heading", level=2)
            # Just wait for it to be visible
            expect(first_q).to_be_visible()

            # Take screenshot of Quiz screen
            page.screenshot(path="verification/quiz_screen.png")
            print("Quiz screen captured.")

            # 5. Answer all questions to reach result
            # There are 12 questions.
            for i in range(12):
                # Click "Strongly Agree" (value 7) or "完全符合"
                # Locate the last option (usually the bottom one)
                options = page.locator("button.group")
                # Wait for options to be ready
                expect(options.first).to_be_visible()

                # Click the last one (Strongly Agree) to force a specific result (likely EROS or similar if all are high?
                # Actually different questions target different dimensions. If we click "Agree" on all, we might get a tie or specific one.
                # Let's click random or specific to get EROS.
                # Q1 is EROS. Q7 is EROS.
                # Let's just click the last option for everything.
                options.last.click()

                # Wait a bit for transition if needed, though app has 250ms delay
                page.wait_for_timeout(300)

            # 6. Wait for calculating
            page.wait_for_timeout(2000)

            # 7. Verify Result Screen
            # Should show a result type.
            result_title = page.get_by_role("heading", level=1)
            expect(result_title).to_be_visible()

            # Take screenshot of Result screen
            page.screenshot(path="verification/result_screen.png")
            print("Result screen captured.")

            # 8. Go to Library
            library_btn = page.get_by_role("button", name="Explore Other Types") # or "了解其他类型"
            if not library_btn.is_visible():
                 library_btn = page.get_by_role("button", name="了解其他类型")

            library_btn.click()

            # 9. Verify Library has tabs
            tab_attach = page.get_by_text("Attachment Theory") # or "依恋理论"
            tab_love = page.get_by_text("Love Styles") # or "爱情色轮" or "Color Wheel"

            # Just check visuals
            page.wait_for_timeout(500)
            page.screenshot(path="verification/library_screen.png")
            print("Library screen captured.")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_love_style_test()
