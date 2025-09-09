import { test, expect } from '@playwright/test';

test.describe('Register', () => {
  test('errors', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    await page
      .getByRole('navigation')
      .getByRole('link')
      .filter({ hasText: /^$/ })
      .click();
    await page.getByRole('link', { name: 'Create an account' }).click();
    await page.getByRole('button', { name: 'Create Account' }).click();
    await expect(
      page.getByTestId('name').getByText('The field is required')
    ).toBeVisible();
    await expect(
      page.getByTestId('paternal_last_name').getByText('The field is required')
    ).toBeVisible();
    await expect(
      page.getByTestId('maternal_last_name').getByText('The field is required')
    ).toBeVisible();
    await expect(
      page.getByTestId('cellphone').getByText('The field is required')
    ).toBeVisible();
    await expect(
      page.getByTestId('municipality_id').getByText('The field is required')
    ).toBeVisible();
    await expect(
      page.getByTestId('email').getByText('The field is required')
    ).toBeVisible();
    await expect(page.getByText('The password must be')).toBeVisible();
    await expect(
      page.getByTestId('confirmPassword').getByText('The field is required')
    ).toBeVisible();
    await expect(
      page.getByTestId('privacy').getByText('The field is required')
    ).toBeVisible();
  });

  test('success', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    await page
      .getByRole('navigation')
      .getByRole('link')
      .filter({ hasText: /^$/ })
      .click();
    await page.getByRole('link', { name: 'Create an account' }).click();
    await page
      .getByTestId('name')
      .getByRole('textbox', { name: 'Name' })
      .fill('L');
    await page
      .getByTestId('name')
      .getByRole('textbox', { name: 'Name' })
      .press('Tab');
    await page.getByRole('textbox', { name: 'First Last Name' }).fill('S');
    await page.getByRole('textbox', { name: 'First Last Name' }).press('Tab');
    await page.getByRole('textbox', { name: 'Second Last Name' }).fill('S');
    await page.getByRole('textbox', { name: 'Second Last Name' }).press('Tab');
    await page
      .getByRole('textbox', { name: 'Cellphone Number' })
      .fill('3331231212');
    await page.getByRole('textbox', { name: 'Cellphone Number' }).press('Tab');
    await page.getByRole('textbox', { name: 'CURP' }).fill('1');
    await page.getByRole('textbox', { name: 'CURP' }).press('Tab');
    await page.getByRole('textbox', { name: 'Email' }).fill('email@com.co');
    await page.getByRole('textbox', { name: 'Email' }).press('Tab');
    await page
      .getByTestId('password')
      .getByRole('textbox', { name: 'Password' })
      .fill('Password1!');
    await page
      .getByTestId('password')
      .getByRole('textbox', { name: 'Password' })
      .press('Tab');
    await page
      .getByRole('textbox', { name: 'Confirm Password' })
      .fill('Password1!');
    await page.getByRole('textbox', { name: 'Confirm Password' }).press('Tab');
    await page
      .getByRole('checkbox', { name: 'I have read the privacy notice' })
      .check();
    await page.getByRole('button', { name: 'Create Account' }).click();

    await expect(page.getByRole('paragraph')).toContainText(
      'Account created successfully!'
    );

    await expect(page).toHaveURL(/.*\/login/);
  });
});
