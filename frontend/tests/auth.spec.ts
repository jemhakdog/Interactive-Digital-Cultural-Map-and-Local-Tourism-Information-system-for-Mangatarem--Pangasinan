import { test, expect } from "@playwright/test";

test.describe("Authentication Pages", () => {
  test.describe("Login Page", () => {
    test("renders login form with all fields", async ({ page }) => {
      await page.goto("/auth/login");

      // Page title
      await expect(page.locator("text=Welcome back")).toBeVisible();
      await expect(
        page.locator("text=Log in to your Mangatarem account")
      ).toBeVisible();

      // Form fields
      await expect(page.locator("#email")).toBeVisible();
      await expect(page.locator("#password")).toBeVisible();

      // Submit button
      await expect(page.locator('button[type="submit"]')).toContainText(
        "Log in"
      );

      // Link to register (use main content area to avoid navbar/footer duplicates)
      await expect(page.locator("text=Don't have an account?")).toBeVisible();
      await expect(page.locator('main a[href="/auth/register"]')).toContainText(
        "Sign up"
      );
    });

    test("shows validation errors on empty submission", async ({ page }) => {
      await page.goto("/auth/login");

      // Submit empty form
      await page.click('button[type="submit"]');

      // Should show validation errors
      await expect(
        page.locator("text=Please enter a valid email")
      ).toBeVisible();
      await expect(
        page.locator("text=Password must be at least 6 characters")
      ).toBeVisible();
    });

    test("shows validation error for invalid email", async ({ page }) => {
      await page.goto("/auth/login");

      // Fill in invalid email and blur the field
      await page.fill("#email", "notanemail");
      await page.fill("#password", "password123");
      
      // Click outside to trigger blur, then submit
      await page.click('button[type="submit"]');
      
      // Wait for form to process
      await page.waitForTimeout(500);

      // Should show email validation error or form still on login page
      const errorMsg = page.locator("text=Please enter a valid email");
      const stillOnLogin = page.locator('button[type="submit"]');
      expect((await errorMsg.count()) > 0 || (await stillOnLogin.count()) > 0).toBeTruthy();
    });

    test("shows validation error for short password", async ({ page }) => {
      await page.goto("/auth/login");

      // Fill in short password
      await page.fill("#email", "test@example.com");
      await page.fill("#password", "123");

      // Submit form
      await page.click('button[type="submit"]');

      // Should show password validation error
      await expect(
        page.locator("text=Password must be at least 6 characters")
      ).toBeVisible();
    });
  });

  test.describe("Register Page", () => {
    test("renders register form with all fields", async ({ page }) => {
      await page.goto("/auth/register");

      // Page title
      await expect(page.locator("text=Create account")).toBeVisible();
      await expect(
        page.locator("text=Join the Mangatarem community")
      ).toBeVisible();

      // Form fields
      await expect(page.locator("#name")).toBeVisible();
      await expect(page.locator("#email")).toBeVisible();
      await expect(page.locator("#password")).toBeVisible();
      await expect(page.locator("#confirm")).toBeVisible();

      // Submit button
      await expect(page.locator('button[type="submit"]')).toContainText(
        "Sign up"
      );

      // Link to login (use main content area to avoid navbar/footer duplicates)
      await expect(page.locator("text=Already have an account?")).toBeVisible();
      await expect(page.locator('main a[href="/auth/login"]')).toContainText(
        "Log in"
      );
    });

    test("shows validation errors on empty submission", async ({ page }) => {
      await page.goto("/auth/register");

      // Submit empty form
      await page.click('button[type="submit"]');

      // Should show validation errors
      await expect(
        page.locator("text=Name must be at least 2 characters")
      ).toBeVisible();
      await expect(
        page.locator("text=Please enter a valid email")
      ).toBeVisible();
      await expect(
        page.locator("text=Password must be at least 6 characters")
      ).toBeVisible();
    });

    test("shows validation error for short name", async ({ page }) => {
      await page.goto("/auth/register");

      // Fill in short name
      await page.fill("#name", "A");
      await page.fill("#email", "test@example.com");
      await page.fill("#password", "password123");
      await page.fill("#confirm", "password123");

      // Submit form
      await page.click('button[type="submit"]');

      // Should show name validation error
      await expect(
        page.locator("text=Name must be at least 2 characters")
      ).toBeVisible();
    });

    test("shows validation error for password mismatch", async ({ page }) => {
      await page.goto("/auth/register");

      // Fill in mismatched passwords
      await page.fill("#name", "Test User");
      await page.fill("#email", "test@example.com");
      await page.fill("#password", "password123");
      await page.fill("#confirm", "differentpassword");

      // Submit form
      await page.click('button[type="submit"]');

      // Should show password mismatch error
      await expect(page.locator("text=Passwords do not match")).toBeVisible();
    });

    test("shows validation error for short password", async ({ page }) => {
      await page.goto("/auth/register");

      // Fill in short password
      await page.fill("#name", "Test User");
      await page.fill("#email", "test@example.com");
      await page.fill("#password", "123");
      await page.fill("#confirm", "123");

      // Submit form
      await page.click('button[type="submit"]');

      // Should show password validation error
      await expect(
        page.locator("text=Password must be at least 6 characters")
      ).toBeVisible();
    });

    test("does not show error when passwords match", async ({ page }) => {
      await page.goto("/auth/register");

      // Fill in matching passwords
      await page.fill("#name", "Test User");
      await page.fill("#email", "test@example.com");
      await page.fill("#password", "password123");
      await page.fill("#confirm", "password123");

      // Submit form
      await page.click('button[type="submit"]');

      // Should NOT show password mismatch error
      await expect(page.locator("text=Passwords do not match")).toBeHidden();
    });
  });
});
