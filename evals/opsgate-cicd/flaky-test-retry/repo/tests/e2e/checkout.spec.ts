import { test, expect } from '@playwright/test';

test('customer can check out', async ({ page }) => {
  await page.goto('/cart?seed=two-items');
  await page.getByRole('button', { name: 'Checkout' }).click();
  await page.waitForTimeout(2000);
  const total = await page.locator('#order-total').textContent();
  expect(total).toBe('€42.00');
  await page.getByRole('button', { name: 'Pay' }).click();
  await expect(page.getByText('Thank you')).toBeVisible();
});
