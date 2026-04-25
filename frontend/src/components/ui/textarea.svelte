<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let value = '';
  export let placeholder = '';
  export let disabled = false;
  export let readonly = false;
  export let required = false;
  export let rows = 3;
  export let className = '';
  export let oninput: ((event: Event) => void) | undefined = undefined;
  export let onchange: ((event: Event) => void) | undefined = undefined;
  export let onkeydown: ((event: KeyboardEvent) => void) | undefined = undefined;
  export let onfocus: ((event: FocusEvent) => void) | undefined = undefined;
  export let onblur: ((event: FocusEvent) => void) | undefined = undefined;
  
  // Computed classes
  $: textareaClass = cn(
    "resize-none border-input placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive dark:bg-input/30 flex field-sizing-content min-h-16 w-full rounded-md border bg-input-background px-3 py-2 text-base transition-[color,box-shadow] outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
    className
  );
</script>

<textarea
  {value}
  {placeholder}
  {disabled}
  {readonly}
  {required}
  {rows}
  class={textareaClass}
  oninput={oninput}
  onchange={onchange}
  onkeydown={onkeydown}
  onfocus={onfocus}
  onblur={onblur}
  {...$$restProps}
></textarea>
