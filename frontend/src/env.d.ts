/// <reference types="astro/client" />
/// <reference types="@astrojs/svelte" />

declare namespace App {
  interface Locals {
    user: {
      id: number;
      email: string;
      full_name?: string;
      is_active: boolean;
    };
  }
}