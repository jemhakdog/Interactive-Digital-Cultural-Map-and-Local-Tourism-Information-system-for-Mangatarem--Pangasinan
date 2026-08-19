import { test, expect } from "@playwright/test";

test.describe("Public Pages", () => {
  test.describe("Attractions Page", () => {
    test("loads and displays page header", async ({ page }) => {
      await page.goto("/attractions");
      await expect(page.locator("h1")).toContainText("Attractions");
      await expect(
        page.locator("text=Discover the beauty and culture of Mangatarem")
      ).toBeVisible();
    });

    test("shows attraction cards or empty state", async ({ page }) => {
      await page.goto("/attractions");
      await page.waitForLoadState("networkidle");

      // Either attraction cards exist or empty state is shown
      const cards = page.locator('[class*="grid"] >> a[href^="/attractions/"]');
      const emptyState = page.locator("text=No attractions found");
      const hasCards = (await cards.count()) > 0;
      const hasEmpty = await emptyState.isVisible();

      expect(hasCards || hasEmpty).toBeTruthy();
    });
  });

  test.describe("Events Page", () => {
    test("loads and displays page header", async ({ page }) => {
      await page.goto("/events");
      await expect(page.locator("h1")).toContainText("Events");
      await expect(
        page.locator("text=What's happening in Mangatarem")
      ).toBeVisible();
    });

    test("shows event cards or empty state", async ({ page }) => {
      await page.goto("/events");
      await page.waitForLoadState("networkidle");

      const cards = page.locator('[class*="grid"] >> a[href^="/events/"]');
      const emptyState = page.locator("text=No events found");
      const hasCards = (await cards.count()) > 0;
      const hasEmpty = await emptyState.isVisible();

      expect(hasCards || hasEmpty).toBeTruthy();
    });
  });

  test.describe("Business Page", () => {
    test("loads and displays page header", async ({ page }) => {
      await page.goto("/business");
      await expect(page.getByRole("heading", { name: "Business Directory" })).toBeVisible();
      await expect(
        page.locator("text=Discover certified accommodations").first()
      ).toBeVisible();
    });

    test("shows business cards or empty state", async ({ page }) => {
      await page.goto("/business");
      await page.waitForLoadState("networkidle");

      const cards = page.locator('[class*="grid"] >> a[href^="/business/"]');
      const emptyState = page.locator("text=No businesses found");
      const hasCards = (await cards.count()) > 0;
      const hasEmpty = await emptyState.isVisible();

      expect(hasCards || hasEmpty).toBeTruthy();
    });
  });

  test.describe("Heritage Page", () => {
    test("loads and displays page header", async ({ page }) => {
      await page.goto("/heritage");
      await expect(page.getByRole("heading", { name: "Heritage Registry" })).toBeVisible();
      await expect(
        page.locator("text=Living History & Cultural Memory").first()
      ).toBeVisible();
    });

    test("shows heritage types or empty state", async ({ page }) => {
      await page.goto("/heritage");
      await page.waitForLoadState("networkidle");

      const cards = page.locator('[class*="grid"] >> a[href^="/heritage/"]');
      const emptyState = page.locator("text=No heritage types found");
      const hasCards = (await cards.count()) > 0;
      const hasEmpty = await emptyState.isVisible();

      expect(hasCards || hasEmpty).toBeTruthy();
    });
  });

  test.describe("Gallery Page", () => {
    test("loads and displays page header", async ({ page }) => {
      await page.goto("/gallery");
      await expect(page.getByRole("heading", { name: "Gallery" })).toBeVisible();
      await expect(page.locator("text=Photos from Mangatarem").first()).toBeVisible();
    });

    test("shows gallery grid or empty state", async ({ page }) => {
      await page.goto("/gallery");
      await page.waitForLoadState("networkidle");

      const grid = page.locator('[class*="grid"]');
      const emptyState = page.locator("text=No gallery items");
      const hasGrid = (await grid.count()) > 0;
      const hasEmpty = await emptyState.isVisible();

      expect(hasGrid || hasEmpty).toBeTruthy();
    });
  });

  test.describe("Map Page", () => {
    test("loads and displays map container", async ({ page }) => {
      await page.goto("/map");
      await expect(page.locator("h1")).toContainText("Map");
      await expect(
        page.locator("text=Explore Mangatarem on the interactive map")
      ).toBeVisible();
    });

    test("shows category filter dropdown", async ({ page }) => {
      await page.goto("/map");
      const select = page.locator("select").first();
      await expect(select).toBeVisible();

      // Check select has options (options are not visible in headless, just check select works)
      await expect(select).toHaveValue("all");
      // Check it has the expected options count
      const optionCount = await select.locator("option").count();
      expect(optionCount).toBeGreaterThanOrEqual(4);
    });

    test("shows map area or loading state", async ({ page }) => {
      await page.goto("/map");
      await page.waitForLoadState("networkidle");

      const mapArea = page.locator('[class*="rounded-lg"][class*="border"]').first();
      const loadingState = page.locator("text=Loading map...");
      const hasMap = (await mapArea.count()) > 0;
      const hasLoading = await loadingState.isVisible();

      expect(hasMap || hasLoading).toBeTruthy();
    });
  });

  test.describe("Search Page", () => {
    test("loads with search input", async ({ page }) => {
      await page.goto("/search");
      await expect(page.locator("h1")).toContainText("Search");

      const searchInput = page.locator('input[placeholder*="Search"]');
      await expect(searchInput).toBeVisible();
      await expect(searchInput).toBeFocused();
    });

    test("search input accepts text", async ({ page }) => {
      await page.goto("/search");
      const searchInput = page.locator('input[placeholder*="Search"]');
      await searchInput.fill("attraction");
      await expect(searchInput).toHaveValue("attraction");
    });
  });

  test.describe("Attraction Detail Page", () => {
    test("loads with reviews section for existing attraction", async ({ page }) => {
      // First, check if there are any attractions to navigate to
      await page.goto("/attractions");
      await page.waitForLoadState("networkidle");

      const attractionLinks = page.locator('a[href^="/attractions/"]');
      const count = await attractionLinks.count();

      if (count > 0) {
        // Navigate to first attraction
        await attractionLinks.first().click();
        await page.waitForLoadState("networkidle");

        // Should show attraction name
        const name = page.locator("h1");
        await expect(name).toBeVisible();

        // Should show reviews section heading
        await expect(page.getByRole("heading", { name: "Reviews" })).toBeVisible();

        // Should have back link
        await expect(page.locator("text=Back to Attractions")).toBeVisible();
      } else {
        // If no attractions, test with ID 2 directly
        await page.goto("/attractions/2");
        // Should show either content or 404
        const isNotFound = page.locator("text=This page could not be found");
        const hasContent = page.locator("h1").first();
        const notFound = await isNotFound.isVisible();
        const hasContentVisible = await hasContent.isVisible();
        expect(notFound || hasContentVisible).toBeTruthy();
      }
    });
  });
});
