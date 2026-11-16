import { test, expect } from '@playwright/test';

test('customer can log in', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('correct-horse');
  await page.getByRole('button', { name: 'Log in' }).click();
  await expect(page.getByText('Welcome back')).toBeVisible();
});
