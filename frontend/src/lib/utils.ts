import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Helper for creating variant-based components in Svelte
export function createVariants<T extends Record<string, Record<string, string>>>(
  base: string,
  variants: T,
  defaultVariants?: Partial<{ [K in keyof T]: keyof T[K] }>
) {
  return (props: { [K in keyof T]?: keyof T[K] } & { class?: string }) => {
    let classes = base;

    for (const [key, value] of Object.entries(props)) {
      if (value && variants[key as keyof T] && variants[key as keyof T][value as string]) {
        classes += ' ' + variants[key as keyof T][value as string];
      }
    }

    // Apply default variants
    if (defaultVariants) {
      for (const [key, value] of Object.entries(defaultVariants)) {
        if (!props[key as keyof T] && variants[key as keyof T] && value) {
          classes += ' ' + variants[key as keyof T][value as string];
        }
      }
    }

    if (props.class) {
      classes += ' ' + props.class;
    }

    return classes;
  };
}
