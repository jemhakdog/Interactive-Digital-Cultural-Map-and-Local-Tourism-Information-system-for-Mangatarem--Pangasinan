import { test, expect } from "@playwright/test";

test.describe("Navigation", () => {
  test("homepage loads with hero text", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("text=Discover Mangatarem")).toBeVisible();
    await expect(
      page.locator("text=Explore the cultural heritage, natural wonders")
    ).toBeVisible();
  });

  test("navigation links are visible in desktop nav", async ({ page }) => {
    await page.goto("/");
    const nav = page.locator("nav").first();
    await expect(nav.locator("text=Attractions")).toBeVisible();
    await expect(nav.locator("text=Events")).toBeVisible();
    await expect(nav.locator("text=Business")).toBeVisible();
    await expect(nav.locator("text=Map")).toBeVisible();
    await expect(nav.locator("text=Heritage")).toBeVisible();
    await expect(nav.locator("text=Gallery")).toBeVisible();
  });

  test("navigate to attractions page", async ({ page }) => {
    await page.goto("/");
    await page.click("nav >> text=Attractions");
    await expect(page).toHaveURL(/\/attractions/);
    await expect(page.locator("h1")).toContainText("Attractions");
  });

  test("navigate to events page", async ({ page }) => {
    await page.goto("/");
    await page.click("nav >> text=Events");
    await expect(page).toHaveURL(/\/events/);
    await expect(page.locator("h1")).toContainText("Events");
  });

  test("navigate to business page", async ({ page }) => {
    await page.goto("/");
    await page.click("nav >> text=Business");
    await expect(page).toHaveURL(/\/business/);
    await expect(page.locator("h1")).toContainText("Business");
  });

  test("navigate to map page", async ({ page }) => {
    await page.goto("/");
    await page.click("nav >> text=Map");
    await expect(page).toHaveURL(/\/map/);
    await expect(page.locator("h1")).toContainText("Map");
  });

  test("navigate to heritage page", async ({ page }) => {
    await page.goto("/");
    await page.click("nav >> text=Heritage");
    await expect(page).toHaveURL(/\/heritage/);
    await expect(page.locator("h1")).toContainText("Heritage");
  });

  test("navigate to gallery page", async ({ page }) => {
    await page.goto("/");
    await page.click("nav >> text=Gallery");
    await expect(page).toHaveURL(/\/gallery/);
    await expect(page.locator("h1")).toContainText("Gallery");
  });

  test("footer links exist", async ({ page }) => {
    await page.goto("/");
    const footer = page.locator("footer");
    await expect(footer).toBeVisible();

    // Explore section - use links to avoid strict mode violations
    await expect(footer.getByRole("link", { name: "Attractions" })).toBeVisible();
    await expect(footer.getByRole("link", { name: "Events" })).toBeVisible();
    await expect(footer.getByRole("link", { name: "Businesses" })).toBeVisible();
    await expect(footer.getByRole("link", { name: "Heritage" })).toBeVisible();
    await expect(footer.getByRole("link", { name: "Map" })).toBeVisible();

    // Community section
    await expect(footer.getByRole("link", { name: "Gallery" })).toBeVisible();
    await expect(footer.getByRole("link", { name: "Chat" })).toBeVisible();

    // Account section
    await expect(footer.getByRole("link", { name: "Log in" })).toBeVisible();
    await expect(footer.getByRole("link", { name: "Sign up" })).toBeVisible();
  });

  test("mobile menu toggle works", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    // Desktop nav should be hidden
    const desktopNav = page.locator("nav.hidden");
    await expect(desktopNav).toBeHidden();

    // Mobile menu button should be visible
    const menuButton = page.locator("button.md\\:hidden").first();
    await expect(menuButton).toBeVisible();

    // Open mobile menu
    await menuButton.click();

    // Mobile nav should appear with links
    const mobileNav = page.locator("div.md\\:hidden >> text=Attractions");
    await expect(mobileNav).toBeVisible();
  });
});
